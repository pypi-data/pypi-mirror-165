import sys
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Callable, Mapping, NamedTuple, Optional, Sequence, cast

from graphql.execution.base import ResolveInfo

import dagster._check as check
from dagster._core.definitions.events import AssetKey
from dagster._core.host_representation import GraphSelector, PipelineSelector
from dagster._core.workspace.context import BaseWorkspaceRequestContext
from dagster._utils.error import serializable_error_info_from_exc_info


def check_permission(permission):
    def decorator(fn):
        def _fn(self, graphene_info, *args, **kwargs):  # pylint: disable=unused-argument
            assert_permission(graphene_info, permission)

            return fn(self, graphene_info, *args, **kwargs)

        return _fn

    return decorator


def assert_permission(graphene_info: ResolveInfo, permission: str) -> None:
    from dagster_graphql.schema.errors import GrapheneUnauthorizedError

    context = cast(BaseWorkspaceRequestContext, graphene_info.context)
    if not context.has_permission(permission):
        raise UserFacingGraphQLError(GrapheneUnauthorizedError())


def _noop(_):
    pass


class ErrorCapture:
    @staticmethod
    def default_on_exception(exc_info):
        from dagster_graphql.schema.errors import GraphenePythonError

        # Transform exception in to PythonError to present to user
        return GraphenePythonError(serializable_error_info_from_exc_info(exc_info))

    # global behavior for how to handle unexpected exceptions
    on_exception = default_on_exception

    # context var for observing unexpected exceptions
    observer: ContextVar[Callable[[Exception], None]] = ContextVar(
        "error_capture_observer", default=_noop
    )

    @staticmethod
    @contextmanager
    def watch(fn: Callable[[Exception], None]):
        token = ErrorCapture.observer.set(fn)
        try:
            yield
        finally:
            ErrorCapture.observer.reset(token)


def capture_error(fn):
    def _fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except UserFacingGraphQLError as de_exception:
            return de_exception.error
        except Exception as exc:
            ErrorCapture.observer.get()(exc)
            return ErrorCapture.on_exception(sys.exc_info())

    return _fn


class UserFacingGraphQLError(Exception):
    def __init__(self, error):
        self.error = error
        message = "[{cls}] {message}".format(
            cls=error.__class__.__name__,
            message=error.message if hasattr(error, "message") else None,
        )
        super(UserFacingGraphQLError, self).__init__(message)


def pipeline_selector_from_graphql(data):
    asset_selection = data.get("assetSelection")
    return PipelineSelector(
        location_name=data["repositoryLocationName"],
        repository_name=data["repositoryName"],
        pipeline_name=data.get("pipelineName") or data.get("jobName"),
        solid_selection=data.get("solidSelection"),
        asset_selection=[AssetKey.from_graphql_input(asset_key) for asset_key in asset_selection]
        if asset_selection
        else None,
    )


def graph_selector_from_graphql(data):
    return GraphSelector(
        location_name=data["repositoryLocationName"],
        repository_name=data["repositoryName"],
        graph_name=data["graphName"],
    )


class ExecutionParams(
    NamedTuple(
        "_ExecutionParams",
        [
            ("selector", PipelineSelector),
            ("run_config", Mapping[str, object]),
            ("mode", Optional[str]),
            ("execution_metadata", "ExecutionMetadata"),
            ("step_keys", Optional[Sequence[str]]),
        ],
    )
):
    def __new__(
        cls,
        selector: PipelineSelector,
        run_config: Optional[Mapping[str, object]],
        mode: Optional[str],
        execution_metadata: "ExecutionMetadata",
        step_keys: Optional[Sequence[str]],
    ):
        check.opt_list_param(step_keys, "step_keys", of_type=str)

        return super(ExecutionParams, cls).__new__(
            cls,
            selector=check.inst_param(selector, "selector", PipelineSelector),
            run_config=check.opt_dict_param(run_config, "run_config", key_type=str),
            mode=check.opt_str_param(mode, "mode"),
            execution_metadata=check.inst_param(
                execution_metadata, "execution_metadata", ExecutionMetadata
            ),
            step_keys=step_keys,
        )

    def to_graphql_input(self):
        return {
            "selector": self.selector.to_graphql_input(),
            "runConfigData": self.run_config,
            "mode": self.mode,
            "executionMetadata": self.execution_metadata.to_graphql_input(),
            "stepKeys": self.step_keys,
        }


class ExecutionMetadata(
    NamedTuple(
        "_ExecutionMetadata",
        [
            ("run_id", Optional[str]),
            ("tags", Mapping[str, str]),
            ("root_run_id", Optional[str]),
            ("parent_run_id", Optional[str]),
        ],
    )
):
    def __new__(
        cls,
        run_id: Optional[str],
        tags: Mapping[str, str],
        root_run_id: Optional[str] = None,
        parent_run_id: Optional[str] = None,
    ):
        return super(ExecutionMetadata, cls).__new__(
            cls,
            check.opt_str_param(run_id, "run_id"),
            check.dict_param(tags, "tags", key_type=str, value_type=str),
            check.opt_str_param(root_run_id, "root_run_id"),
            check.opt_str_param(parent_run_id, "parent_run_id"),
        )

    def to_graphql_input(self):
        return {
            "runId": self.run_id,
            "tags": [{"key": k, "value": v} for k, v in self.tags.items()],
            "rootRunId": self.root_run_id,
            "parentRunId": self.parent_run_id,
        }
