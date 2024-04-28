# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromadb/proto/logservice.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromadb.proto import chroma_pb2 as chromadb_dot_proto_dot_chroma__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x63hromadb/proto/logservice.proto\x12\x06\x63hroma\x1a\x1b\x63hromadb/proto/chroma.proto\"R\n\x0fPushLogsRequest\x12\x15\n\rcollection_id\x18\x01 \x01(\t\x12(\n\x07records\x18\x02 \x03(\x0b\x32\x17.chroma.OperationRecord\"(\n\x10PushLogsResponse\x12\x14\n\x0crecord_count\x18\x01 \x01(\x05\"n\n\x0fPullLogsRequest\x12\x15\n\rcollection_id\x18\x01 \x01(\t\x12\x19\n\x11start_from_offset\x18\x02 \x01(\x03\x12\x12\n\nbatch_size\x18\x03 \x01(\x05\x12\x15\n\rend_timestamp\x18\x04 \x01(\x03\"H\n\tLogRecord\x12\x12\n\nlog_offset\x18\x01 \x01(\x03\x12\'\n\x06record\x18\x02 \x01(\x0b\x32\x17.chroma.OperationRecord\"6\n\x10PullLogsResponse\x12\"\n\x07records\x18\x01 \x03(\x0b\x32\x11.chroma.LogRecord\"W\n\x0e\x43ollectionInfo\x12\x15\n\rcollection_id\x18\x01 \x01(\t\x12\x18\n\x10\x66irst_log_offset\x18\x02 \x01(\x03\x12\x14\n\x0c\x66irst_log_ts\x18\x03 \x01(\x03\"&\n$GetAllCollectionInfoToCompactRequest\"\\\n%GetAllCollectionInfoToCompactResponse\x12\x33\n\x13\x61ll_collection_info\x18\x01 \x03(\x0b\x32\x16.chroma.CollectionInfo\"M\n UpdateCollectionLogOffsetRequest\x12\x15\n\rcollection_id\x18\x01 \x01(\t\x12\x12\n\nlog_offset\x18\x02 \x01(\x03\"#\n!UpdateCollectionLogOffsetResponse2\x82\x03\n\nLogService\x12?\n\x08PushLogs\x12\x17.chroma.PushLogsRequest\x1a\x18.chroma.PushLogsResponse\"\x00\x12?\n\x08PullLogs\x12\x17.chroma.PullLogsRequest\x1a\x18.chroma.PullLogsResponse\"\x00\x12~\n\x1dGetAllCollectionInfoToCompact\x12,.chroma.GetAllCollectionInfoToCompactRequest\x1a-.chroma.GetAllCollectionInfoToCompactResponse\"\x00\x12r\n\x19UpdateCollectionLogOffset\x12(.chroma.UpdateCollectionLogOffsetRequest\x1a).chroma.UpdateCollectionLogOffsetResponse\"\x00\x42\x39Z7github.com/chroma-core/chroma/go/pkg/proto/logservicepbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromadb.proto.logservice_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z7github.com/chroma-core/chroma/go/pkg/proto/logservicepb'
  _globals['_PUSHLOGSREQUEST']._serialized_start=72
  _globals['_PUSHLOGSREQUEST']._serialized_end=154
  _globals['_PUSHLOGSRESPONSE']._serialized_start=156
  _globals['_PUSHLOGSRESPONSE']._serialized_end=196
  _globals['_PULLLOGSREQUEST']._serialized_start=198
  _globals['_PULLLOGSREQUEST']._serialized_end=308
  _globals['_LOGRECORD']._serialized_start=310
  _globals['_LOGRECORD']._serialized_end=382
  _globals['_PULLLOGSRESPONSE']._serialized_start=384
  _globals['_PULLLOGSRESPONSE']._serialized_end=438
  _globals['_COLLECTIONINFO']._serialized_start=440
  _globals['_COLLECTIONINFO']._serialized_end=527
  _globals['_GETALLCOLLECTIONINFOTOCOMPACTREQUEST']._serialized_start=529
  _globals['_GETALLCOLLECTIONINFOTOCOMPACTREQUEST']._serialized_end=567
  _globals['_GETALLCOLLECTIONINFOTOCOMPACTRESPONSE']._serialized_start=569
  _globals['_GETALLCOLLECTIONINFOTOCOMPACTRESPONSE']._serialized_end=661
  _globals['_UPDATECOLLECTIONLOGOFFSETREQUEST']._serialized_start=663
  _globals['_UPDATECOLLECTIONLOGOFFSETREQUEST']._serialized_end=740
  _globals['_UPDATECOLLECTIONLOGOFFSETRESPONSE']._serialized_start=742
  _globals['_UPDATECOLLECTIONLOGOFFSETRESPONSE']._serialized_end=777
  _globals['_LOGSERVICE']._serialized_start=780
  _globals['_LOGSERVICE']._serialized_end=1166
# @@protoc_insertion_point(module_scope)
