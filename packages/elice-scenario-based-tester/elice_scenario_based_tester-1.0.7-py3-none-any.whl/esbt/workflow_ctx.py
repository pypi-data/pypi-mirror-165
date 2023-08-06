from __future__ import annotations

import contextlib
import contextvars
import uuid
from typing import TYPE_CHECKING, Dict, Iterator, NamedTuple, Union

if TYPE_CHECKING:
    from aiohttp import ClientSession

    from esbt.model import ScenarioBase


_current_workflow_ctx_var: contextvars.ContextVar[WorkflowCtx] = contextvars.ContextVar(
    '_current_workflow_ctx_var')


class _current_workflow_ctx_var_getter:
    def __get__(self, obj, objtype=None):  # type: ignore
        return _current_workflow_ctx_var.get()


class WorkflowCtx(NamedTuple):
    if TYPE_CHECKING:  # type: ignore
        current: WorkflowCtx

    dependency: Dict[tuple[str, ScenarioBase], list[tuple[str, ScenarioBase]]]
    session: ClientSession
    context: Dict[str, Union[str, bool]]

    ctx_id: str | None = None


async def create_workflow_ctx(dependency):
    import aiohttp

    return WorkflowCtx(
        dependency=dependency,
        context={},
        session=aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)),
    )


@contextlib.asynccontextmanager
async def bind_workflow_ctx(workflow_ctx: WorkflowCtx) -> Iterator[None]:
    var_set_token = _current_workflow_ctx_var.set(
        workflow_ctx._replace(ctx_id=str(uuid.uuid4())))
    try:
        yield
    finally:
        _current_workflow_ctx_var.reset(var_set_token)


WorkflowCtx.current = _current_workflow_ctx_var_getter()  # type: ignore
