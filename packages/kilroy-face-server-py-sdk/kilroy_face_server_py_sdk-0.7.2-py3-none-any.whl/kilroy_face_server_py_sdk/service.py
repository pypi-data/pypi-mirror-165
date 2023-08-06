import json
from typing import AsyncIterator, Dict
from uuid import UUID

import grpclib
from betterproto.grpc.grpclib_server import ServiceBase
from grpclib import server
from kilroy_face_py_shared import (
    GetConfigRequest,
    GetConfigResponse,
    GetConfigSchemaRequest,
    GetConfigSchemaResponse,
    GetMetadataRequest,
    GetMetadataResponse,
    GetPostSchemaRequest,
    GetPostSchemaResponse,
    GetStatusRequest,
    GetStatusResponse,
    PostRequest,
    PostResponse,
    RealPost,
    ScoreRequest,
    ScoreResponse,
    ScrapRequest,
    ScrapResponse,
    SetConfigRequest,
    SetConfigResponse,
    Status,
    WatchConfigRequest,
    WatchConfigResponse,
    WatchStatusRequest,
    WatchStatusResponse,
)

from kilroy_face_server_py_sdk import Face


class FaceServiceBase(ServiceBase):
    async def get_metadata(
        self, get_metadata_request: "GetMetadataRequest"
    ) -> "GetMetadataResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_post_schema(
        self, get_post_schema_request: "GetPostSchemaRequest"
    ) -> "GetPostSchemaResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_status(
        self, get_status_request: "GetStatusRequest"
    ) -> "GetStatusResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def watch_status(
        self, watch_status_request: "WatchStatusRequest"
    ) -> AsyncIterator["WatchStatusResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_config_schema(
        self, get_config_schema_request: "GetConfigSchemaRequest"
    ) -> "GetConfigSchemaResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_config(
        self, get_config_request: "GetConfigRequest"
    ) -> "GetConfigResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def watch_config(
        self, watch_config_request: "WatchConfigRequest"
    ) -> AsyncIterator["WatchConfigResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def set_config(
        self, set_config_request: "SetConfigRequest"
    ) -> "SetConfigResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def post(self, post_request: "PostRequest") -> "PostResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def score(self, score_request: "ScoreRequest") -> "ScoreResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def scrap(
        self, scrap_request: "ScrapRequest"
    ) -> AsyncIterator["ScrapResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_get_metadata(
        self,
        stream: "server.Stream[GetMetadataRequest, GetMetadataResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_metadata(request)
        await stream.send_message(response)

    async def __rpc_get_post_schema(
        self,
        stream: "server.Stream[GetPostSchemaRequest, GetPostSchemaResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_post_schema(request)
        await stream.send_message(response)

    async def __rpc_get_status(
        self,
        stream: "server.Stream[GetStatusRequest, GetStatusResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_status(request)
        await stream.send_message(response)

    async def __rpc_watch_status(
        self,
        stream: "server.Stream[WatchStatusRequest, WatchStatusResponse]",
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.watch_status,
            stream,
            request,
        )

    async def __rpc_get_config_schema(
        self,
        stream: "server.Stream[GetConfigSchemaRequest, GetConfigSchemaResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_config_schema(request)
        await stream.send_message(response)

    async def __rpc_get_config(
        self,
        stream: "server.Stream[GetConfigRequest, GetConfigResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_config(request)
        await stream.send_message(response)

    async def __rpc_watch_config(
        self,
        stream: "server.Stream[WatchConfigRequest, WatchConfigResponse]",
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.watch_config,
            stream,
            request,
        )

    async def __rpc_set_config(
        self,
        stream: "server.Stream[SetConfigRequest, SetConfigResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.set_config(request)
        await stream.send_message(response)

    async def __rpc_post(
        self, stream: "server.Stream[PostRequest, PostResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.post(request)
        await stream.send_message(response)

    async def __rpc_score(
        self, stream: "server.Stream[ScoreRequest, ScoreResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.score(request)
        await stream.send_message(response)

    async def __rpc_scrap(
        self, stream: "server.Stream[ScrapRequest, ScrapResponse]"
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.scrap,
            stream,
            request,
        )

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/kilroy.face.v1alpha.FaceService/GetMetadata": grpclib.const.Handler(
                self.__rpc_get_metadata,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetMetadataRequest,
                GetMetadataResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/GetPostSchema": grpclib.const.Handler(
                self.__rpc_get_post_schema,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetPostSchemaRequest,
                GetPostSchemaResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/GetStatus": grpclib.const.Handler(
                self.__rpc_get_status,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetStatusRequest,
                GetStatusResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/WatchStatus": grpclib.const.Handler(
                self.__rpc_watch_status,
                grpclib.const.Cardinality.UNARY_STREAM,
                WatchStatusRequest,
                WatchStatusResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/GetConfigSchema": grpclib.const.Handler(
                self.__rpc_get_config_schema,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetConfigSchemaRequest,
                GetConfigSchemaResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/GetConfig": grpclib.const.Handler(
                self.__rpc_get_config,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetConfigRequest,
                GetConfigResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/WatchConfig": grpclib.const.Handler(
                self.__rpc_watch_config,
                grpclib.const.Cardinality.UNARY_STREAM,
                WatchConfigRequest,
                WatchConfigResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/SetConfig": grpclib.const.Handler(
                self.__rpc_set_config,
                grpclib.const.Cardinality.UNARY_UNARY,
                SetConfigRequest,
                SetConfigResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/Post": grpclib.const.Handler(
                self.__rpc_post,
                grpclib.const.Cardinality.UNARY_UNARY,
                PostRequest,
                PostResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/Score": grpclib.const.Handler(
                self.__rpc_score,
                grpclib.const.Cardinality.UNARY_UNARY,
                ScoreRequest,
                ScoreResponse,
            ),
            "/kilroy.face.v1alpha.FaceService/Scrap": grpclib.const.Handler(
                self.__rpc_scrap,
                grpclib.const.Cardinality.UNARY_STREAM,
                ScrapRequest,
                ScrapResponse,
            ),
        }


class FaceService(FaceServiceBase):
    def __init__(self, face: Face) -> None:
        super().__init__()
        self._face = face

    async def get_metadata(
        self, get_metadata_request: "GetMetadataRequest"
    ) -> "GetMetadataResponse":
        metadata = self._face.metadata
        return GetMetadataResponse().from_dict(
            {
                "key": metadata.key,
                "description": metadata.description,
            }
        )

    async def get_post_schema(
        self, get_post_schema_request: "GetPostSchemaRequest"
    ) -> "GetPostSchemaResponse":
        schema = self._face.post_schema
        return GetPostSchemaResponse().from_dict({"schema": schema.json()})

    async def get_status(
        self, get_status_request: "GetStatusRequest"
    ) -> "GetStatusResponse":
        ready = await self._face.state.ready.fetch()
        status = Status.STATUS_READY if ready else Status.STATUS_LOADING
        return GetStatusResponse().from_dict({"status": status})

    async def watch_status(
        self, watch_status_request: "WatchStatusRequest"
    ) -> AsyncIterator["WatchStatusResponse"]:
        async for ready in self._face.state.ready.subscribe():
            status = Status.STATUS_READY if ready else Status.STATUS_LOADING
            yield WatchStatusResponse().from_dict({"status": status})

    async def get_config_schema(
        self, get_config_schema_request: "GetConfigSchemaRequest"
    ) -> "GetConfigSchemaResponse":
        schema = self._face.schema
        return GetConfigSchemaResponse().from_dict({"schema": schema.json()})

    async def get_config(
        self, get_config_request: "GetConfigRequest"
    ) -> "GetConfigResponse":
        config = await self._face.config.json.fetch()
        return GetConfigResponse().from_dict({"config": json.dumps(config)})

    async def watch_config(
        self, watch_config_request: "WatchConfigRequest"
    ) -> AsyncIterator["WatchConfigResponse"]:
        async for config in self._face.config.json.subscribe():
            yield WatchConfigResponse().from_dict(
                {"config": json.dumps(config)}
            )

    async def set_config(
        self, set_config_request: "SetConfigRequest"
    ) -> "SetConfigResponse":
        config = json.loads(set_config_request.config)
        config = await self._face.config.set(config)
        return SetConfigResponse().from_dict({"config": json.dumps(config)})

    async def post(self, post_request: "PostRequest") -> "PostResponse":
        post = json.loads(post_request.post.content)
        uid = await self._face.post(post)
        return PostResponse().from_dict({"post_id": str(uid)})

    async def score(self, score_request: "ScoreRequest") -> "ScoreResponse":
        score = await self._face.score(UUID(score_request.post_id))
        return ScoreResponse().from_dict({"score": score})

    async def scrap(
        self, scrap_request: "ScrapRequest"
    ) -> AsyncIterator["ScrapResponse"]:
        async for uid, post, score in self._face.scrap(
            scrap_request.limit, scrap_request.before, scrap_request.after
        ):
            yield ScrapResponse(
                post=RealPost(
                    id=str(uid),
                    content=json.dumps(post),
                    score=score,
                ),
            )
