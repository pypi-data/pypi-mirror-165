import json
from abc import abstractmethod
from typing import AsyncIterator, Dict
from uuid import UUID

import aiostream
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase
from grpclib import server
from kilroy_module_py_shared import (
    FitPostsRequest,
    FitPostsResponse,
    FitScoresRequest,
    FitScoresResponse,
    GenerateRequest,
    GenerateResponse,
    GeneratedPost,
    GetConfigRequest,
    GetConfigResponse,
    GetConfigSchemaRequest,
    GetConfigSchemaResponse,
    GetMetadataRequest,
    GetMetadataResponse,
    GetMetricsConfigRequest,
    GetMetricsConfigResponse,
    GetPostSchemaRequest,
    GetPostSchemaResponse,
    GetStatusRequest,
    GetStatusResponse,
    MetricConfig,
    SetConfigRequest,
    SetConfigResponse,
    Status,
    StepRequest,
    StepResponse,
    WatchConfigRequest,
    WatchConfigResponse,
    WatchMetricsRequest,
    WatchMetricsResponse,
    WatchStatusRequest,
    WatchStatusResponse,
)

from kilroy_module_server_py_sdk import Metric, Module


class ModuleServiceBase(ServiceBase):
    @abstractmethod
    async def get_metadata(
        self, get_metadata_request: "GetMetadataRequest"
    ) -> "GetMetadataResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def get_post_schema(
        self, get_post_schema_request: "GetPostSchemaRequest"
    ) -> "GetPostSchemaResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def get_status(
        self, get_status_request: "GetStatusRequest"
    ) -> "GetStatusResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def watch_status(
        self, watch_status_request: "WatchStatusRequest"
    ) -> AsyncIterator["WatchStatusResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def get_config_schema(
        self, get_config_schema_request: "GetConfigSchemaRequest"
    ) -> "GetConfigSchemaResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def get_config(
        self, get_config_request: "GetConfigRequest"
    ) -> "GetConfigResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def watch_config(
        self, watch_config_request: "WatchConfigRequest"
    ) -> AsyncIterator["WatchConfigResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def set_config(
        self, set_config_request: "SetConfigRequest"
    ) -> "SetConfigResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def generate(
        self, generate_request: "GenerateRequest"
    ) -> AsyncIterator["GenerateResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def fit_posts(
        self, fit_posts_request_iterator: AsyncIterator["FitPostsRequest"]
    ) -> "FitPostsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def fit_scores(
        self, fit_scores_request: "FitScoresRequest"
    ) -> "FitScoresResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def step(self, step_request: "StepRequest") -> "StepResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def get_metrics_config(
        self, get_metrics_config_request: "GetMetricsConfigRequest"
    ) -> "GetMetricsConfigResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    @abstractmethod
    async def watch_metrics(
        self, watch_metrics_request: "WatchMetricsRequest"
    ) -> AsyncIterator["WatchMetricsResponse"]:
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

    async def __rpc_generate(
        self,
        stream: "server.Stream[GenerateRequest, GenerateResponse]",
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.generate,
            stream,
            request,
        )

    async def __rpc_fit_posts(
        self,
        stream: "server.Stream[FitPostsRequest, FitPostsResponse]",
    ) -> None:
        request = stream.__aiter__()
        response = await self.fit_posts(request)
        await stream.send_message(response)

    async def __rpc_fit_scores(
        self,
        stream: "server.Stream[FitScoresRequest, FitScoresResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.fit_scores(request)
        await stream.send_message(response)

    async def __rpc_step(
        self, stream: "server.Stream[StepRequest, StepResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.step(request)
        await stream.send_message(response)

    async def __rpc_get_metrics_config(
        self,
        stream: "server.Stream[GetMetricsConfigRequest, GetMetricsConfigResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_metrics_config(request)
        await stream.send_message(response)

    async def __rpc_watch_metrics(
        self,
        stream: "server.Stream[WatchMetricsRequest, WatchMetricsResponse]",
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.watch_metrics,
            stream,
            request,
        )

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/kilroy.module.v1alpha.ModuleService/GetMetadata": grpclib.const.Handler(
                self.__rpc_get_metadata,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetMetadataRequest,
                GetMetadataResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/GetPostSchema": grpclib.const.Handler(
                self.__rpc_get_post_schema,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetPostSchemaRequest,
                GetPostSchemaResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/GetStatus": grpclib.const.Handler(
                self.__rpc_get_status,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetStatusRequest,
                GetStatusResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/WatchStatus": grpclib.const.Handler(
                self.__rpc_watch_status,
                grpclib.const.Cardinality.UNARY_STREAM,
                WatchStatusRequest,
                WatchStatusResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/GetConfigSchema": grpclib.const.Handler(
                self.__rpc_get_config_schema,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetConfigSchemaRequest,
                GetConfigSchemaResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/GetConfig": grpclib.const.Handler(
                self.__rpc_get_config,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetConfigRequest,
                GetConfigResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/WatchConfig": grpclib.const.Handler(
                self.__rpc_watch_config,
                grpclib.const.Cardinality.UNARY_STREAM,
                WatchConfigRequest,
                WatchConfigResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/SetConfig": grpclib.const.Handler(
                self.__rpc_set_config,
                grpclib.const.Cardinality.UNARY_UNARY,
                SetConfigRequest,
                SetConfigResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/Generate": grpclib.const.Handler(
                self.__rpc_generate,
                grpclib.const.Cardinality.UNARY_STREAM,
                GenerateRequest,
                GenerateResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/FitPosts": grpclib.const.Handler(
                self.__rpc_fit_posts,
                grpclib.const.Cardinality.STREAM_UNARY,
                FitPostsRequest,
                FitPostsResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/FitScores": grpclib.const.Handler(
                self.__rpc_fit_scores,
                grpclib.const.Cardinality.UNARY_UNARY,
                FitScoresRequest,
                FitScoresResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/Step": grpclib.const.Handler(
                self.__rpc_step,
                grpclib.const.Cardinality.UNARY_UNARY,
                StepRequest,
                StepResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/GetMetricsConfig": grpclib.const.Handler(
                self.__rpc_get_metrics_config,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetMetricsConfigRequest,
                GetMetricsConfigResponse,
            ),
            "/kilroy.module.v1alpha.ModuleService/WatchMetrics": grpclib.const.Handler(
                self.__rpc_watch_metrics,
                grpclib.const.Cardinality.UNARY_STREAM,
                WatchMetricsRequest,
                WatchMetricsResponse,
            ),
        }


class ModuleService(ModuleServiceBase):
    def __init__(self, module: Module) -> None:
        super().__init__()
        self._module = module

    async def get_metadata(
        self, get_metadata_request: "GetMetadataRequest"
    ) -> "GetMetadataResponse":
        metadata = self._module.metadata
        return GetMetadataResponse().from_dict(
            {
                "key": metadata.key,
                "description": metadata.description,
            }
        )

    async def get_post_schema(
        self, get_post_schema_request: "GetPostSchemaRequest"
    ) -> "GetPostSchemaResponse":
        schema = self._module.post_schema
        return GetPostSchemaResponse().from_dict({"schema": schema.json()})

    async def get_status(
        self, get_status_request: "GetStatusRequest"
    ) -> "GetStatusResponse":
        ready = await self._module.state.ready.fetch()
        status = Status.STATUS_READY if ready else Status.STATUS_LOADING
        return GetStatusResponse().from_dict({"status": status})

    async def watch_status(
        self, watch_status_request: "WatchStatusRequest"
    ) -> AsyncIterator["WatchStatusResponse"]:
        async for ready in self._module.state.ready.subscribe():
            status = Status.STATUS_READY if ready else Status.STATUS_LOADING
            yield WatchStatusResponse().from_dict({"status": status})

    async def get_config_schema(
        self, get_config_schema_request: "GetConfigSchemaRequest"
    ) -> "GetConfigSchemaResponse":
        schema = self._module.schema
        return GetConfigSchemaResponse().from_dict({"schema": schema.json()})

    async def get_config(
        self, get_config_request: "GetConfigRequest"
    ) -> "GetConfigResponse":
        config = await self._module.config.json.fetch()
        return GetConfigResponse().from_dict({"config": json.dumps(config)})

    async def watch_config(
        self, watch_config_request: "WatchConfigRequest"
    ) -> AsyncIterator["WatchConfigResponse"]:
        async for config in self._module.config.json.subscribe():
            yield WatchConfigResponse().from_dict(
                {"config": json.dumps(config)}
            )

    async def set_config(
        self, set_config_request: "SetConfigRequest"
    ) -> "SetConfigResponse":
        config = json.loads(set_config_request.config)
        config = await self._module.config.set(config)
        return SetConfigResponse().from_dict({"config": json.dumps(config)})

    async def generate(
        self, generate_request: "GenerateRequest"
    ) -> AsyncIterator["GenerateResponse"]:
        async for post_id, post in self._module.generate(
            generate_request.quantity, generate_request.dry
        ):
            post = GeneratedPost().from_dict(
                {"id": str(post_id), "content": json.dumps(post)}
            )
            yield GenerateResponse(post=post)

    async def fit_posts(
        self, fit_posts_request_iterator: AsyncIterator["FitPostsRequest"]
    ) -> "FitPostsResponse":
        async def posts():
            async for request in fit_posts_request_iterator:
                yield json.loads(request.post.content), request.post.score

        await self._module.fit_posts(posts())
        return FitPostsResponse()

    async def fit_scores(
        self, fit_scores_request: "FitScoresRequest"
    ) -> "FitScoresResponse":
        scores = [
            (UUID(score.id), score.score)
            for score in fit_scores_request.scores
        ]

        await self._module.fit_scores(scores)
        return FitScoresResponse()

    async def step(self, step_request: "StepRequest") -> "StepResponse":
        await self._module.step()
        return StepResponse()

    async def get_metrics_config(
        self, get_metrics_config_request: "GetMetricsConfigRequest"
    ) -> "GetMetricsConfigResponse":
        configs = [
            MetricConfig().from_dict(
                {
                    "id": metric.name,
                    "label": metric.label,
                    "config": json.dumps(metric.config),
                }
            )
            for metric in await self._module.get_metrics()
        ]
        return GetMetricsConfigResponse(configs=configs)

    async def watch_metrics(
        self, watch_metrics_request: "WatchMetricsRequest"
    ) -> AsyncIterator["WatchMetricsResponse"]:
        async def converted(
            metric: Metric,
        ) -> AsyncIterator["WatchMetricsResponse"]:
            async for dataset_id, data in metric.watch():
                yield WatchMetricsResponse().from_dict(
                    {
                        "metric_id": metric.name,
                        "dataset_id": dataset_id,
                        "data": json.dumps(data),
                    }
                )

        combine = aiostream.stream.merge(
            *(converted(metric) for metric in await self._module.get_metrics())
        )

        async with combine.stream() as streamer:
            async for message in streamer:
                yield message
