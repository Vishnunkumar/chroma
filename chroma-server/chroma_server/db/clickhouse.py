from chroma_server.db.abstract import Database
import uuid
import time
import os

from clickhouse_driver import connect, Client

EMBEDDING_TABLE_SCHEMA = [
    {'model_space': 'String'},
    {'uuid': 'UUID'},
    {'embedding': 'Array(Float64)'},
    {'input_uri': 'String'},
    {'dataset': 'String'},
    {'inference_class': 'String'},
    {'label_class': 'Nullable(String)'},
]

RESULTS_TABLE_SCHEMA = [
    {'model_space': 'String'},
    {'uuid': 'UUID'},
    {'custom_quality_score': ' Nullable(Float64)'},
]

def db_array_schema_to_clickhouse_schema(table_schema):
    return_str = ""
    for element in table_schema:
        for k, v in element.items():
            return_str += f"{k} {v}, "
    return return_str

def db_schema_to_keys():
    return_str = ""
    for element in EMBEDDING_TABLE_SCHEMA:
        if element == EMBEDDING_TABLE_SCHEMA[-1]:
            return_str += f"{list(element.keys())[0]}"
        else:
            return_str += f"{list(element.keys())[0]}, "
    return return_str

def get_col_pos(col_name):
    for i, col in enumerate(EMBEDDING_TABLE_SCHEMA):
        if col_name in col:
            return i

class Clickhouse(Database):
    _conn = None

    def _create_table_embeddings(self):
        self._conn.execute(f'''CREATE TABLE IF NOT EXISTS embeddings (
            {db_array_schema_to_clickhouse_schema(EMBEDDING_TABLE_SCHEMA)}
        ) ENGINE = MergeTree() ORDER BY model_space''')

        self._conn.execute(f'''SET allow_experimental_lightweight_delete = true''')
        self._conn.execute(f'''SET mutations_sync = 1''') # https://clickhouse.com/docs/en/operations/settings/settings/#mutations_sync
    
    def _create_table_results(self):
        self._conn.execute(f'''CREATE TABLE IF NOT EXISTS results (
            {db_array_schema_to_clickhouse_schema(RESULTS_TABLE_SCHEMA)}
        ) ENGINE = MergeTree() ORDER BY model_space''')

    def __init__(self):
        client = Client(host='clickhouse', port=os.getenv('CLICKHOUSE_TCP_PORT', '9000'))
        self._conn = client
        self._create_table_embeddings()
        self._create_table_results()

    def add(self, model_space, embedding, input_uri, dataset=None, inference_class=None, label_class=None):
        data_to_insert = []
        for i in range(len(embedding)):
            data_to_insert.append([model_space[i], uuid.uuid4(), embedding[i], input_uri[i], dataset[i], inference_class[i], (label_class[i] if label_class is not None else None)])

        insert_string = "model_space, uuid, embedding, input_uri, dataset, inference_class, label_class"

        self._conn.execute(f'''
         INSERT INTO embeddings ({insert_string}) VALUES''', data_to_insert)

    def _count(self, model_space=None):
        where_string = ""
        if model_space is not None:
            where_string = f"WHERE model_space = '{model_space}'"
        return self._conn.execute(f"SELECT COUNT() FROM embeddings {where_string}")
        
    def count(self, model_space=None):
        return self._count(model_space=model_space)[0][0]

    def _fetch(self, where={}, columnar=False):
        return self._conn.execute(f'''SELECT {db_schema_to_keys()} FROM embeddings {where}''', columnar=columnar)

    def fetch(self, where={}, sort=None, limit=None, offset=None, columnar=False):
        if where["model_space"] is None:
            return {"error": "model_space is required"}

        s3= time.time()
        # check to see if query is a dict and if it is a flat list of key value pairs
        if where is not None:
            if not isinstance(where, dict):
                raise Exception("Invalid where: " + str(where))
            
            # ensure where is a flat dict
            for key in where:
                if isinstance(where[key], dict):
                    raise Exception("Invalid where: " + str(where))
        
        where = " AND ".join([f"{key} = '{value}'" for key, value in where.items()])

        if where:
            where = f"WHERE {where}"

        if sort is not None:
            where += f" ORDER BY {sort}"
        else:
            where += f" ORDER BY model_space" # stable ordering

        if limit is not None or isinstance(limit, int):
            where += f" LIMIT {limit}"
        
        if offset is not None or isinstance(offset, int):
            where += f" OFFSET {offset}"

        val = self._fetch(where=where, columnar=columnar)
        print(f"time to fetch {len(val)} embeddings: ", time.time() - s3)

        return val

    def _delete(self, where={}):
        return self._conn.execute(f'''
            DELETE FROM 
                embeddings
        {where}
        ''')

    def delete(self, where={}):
        if where["model_space"] is None:
            return {"error": "model_space is required. Use reset to clear the entire db"}

        s3= time.time()
        # check to see if query is a dict and if it is a flat list of key value pairs
        if where is not None:
            if not isinstance(where, dict):
                raise Exception("Invalid where: " + str(where))
            
            # ensure where is a flat dict
            for key in where:
                if isinstance(where[key], dict):
                    raise Exception("Invalid where: " + str(where))
        
        where = " AND ".join([f"{key} = '{value}'" for key, value in where.items()])

        if where:
            where = f"WHERE {where}"

        val = self._delete(where=where)
        print(f"time to fetch {len(val)} embeddings: ", time.time() - s3)

        return val

    def get_by_ids(self, ids=list):
        return self._conn.execute(f'''
            SELECT {db_schema_to_keys()} FROM embeddings WHERE uuid IN ({ids})''')

    def reset(self):
        self._conn.execute('DROP TABLE embeddings')
        self._conn.execute('DROP TABLE results')
        self._create_table_embeddings()
        self._create_table_results()

    def raw_sql(self, sql):
        return self._conn.execute(sql)

    def add_results(self, model_spaces, uuids, custom_quality_score):
        data_to_insert = []
        for i in range(len(model_spaces)):
            data_to_insert.append([model_spaces[i], uuids[i], custom_quality_score[i]])

        self._conn.execute('''
         INSERT INTO results (model_space, uuid, custom_quality_score) VALUES''', data_to_insert)
    
    def delete_results(self, model_space):
        self._conn.execute(f"DELETE FROM results WHERE model_space = '{model_space}'")

    def count_results(self, model_space=None):
        where_string = ""
        if model_space is not None:
            where_string = f"WHERE model_space = '{model_space}'"
        return self._conn.execute(f"SELECT COUNT() FROM results {where_string}")[0][0]
     
    def return_results(self, model_space, n_results = 100):
        return self._conn.execute(f'''
            SELECT
                embeddings.input_uri,
                embeddings.embedding,
                results.custom_quality_score
            FROM
                results
            INNER JOIN
                embeddings
            ON
                results.uuid = embeddings.uuid
            WHERE
                results.model_space = '{model_space}'
            ORDER BY
                results.custom_quality_score DESC
            LIMIT {n_results}
        ''')
