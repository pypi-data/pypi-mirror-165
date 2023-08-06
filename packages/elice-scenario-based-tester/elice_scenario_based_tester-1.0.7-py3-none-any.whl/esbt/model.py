from __future__ import annotations

import asyncio
import re
from io import BufferedReader
from typing import Any, Dict, Literal, Union

from aiohttp import FormData
from .config_proxy import config
from esbt.func import ScenarioException, extract_data_from_res, make_form_data
from esbt.workflow_ctx import WorkflowCtx

FORMAT_STR_RE = r'(?<=\${)(.*?)(?=})'


class Request:
    def __init__(
        self,
        method: Literal['POST', 'GET'],
        url: str,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
        files: Dict[str, tuple[str, str]] | None = None,
        extract_fields: list[str] | None = None,
    ) -> None:
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.headers = headers
        self.files = files
        self.extract_fields = extract_fields or []
        self.opened_files: list[BufferedReader] = []

    def _convert_fields(
        self,
        data: dict[str, str],
        agent: Agent,
        scenario: ScenarioBase,
        repeat_cnt: int,
        files: dict[str, tuple[str, str]] | None = None,
        open_files: list[BufferedReader] | None = None,
    ) -> Union[dict[str, Any], None, FormData]:
        if data is None:
            return None

        new_data = data.copy()

        current_dependency: list[tuple[str, ScenarioBase]] = WorkflowCtx.current.dependency.get(
            (agent.name, scenario.__class__), []
        )

        for k, v in new_data.items():
            extract_fields = re.findall(r'(?<=\${)(.*?)(?=})', str(v))
            if not extract_fields:
                continue

            for field in extract_fields:
                for agent_name, scn_class in current_dependency:
                    cnt = repeat_cnt % WorkflowCtx.current.context.get(
                        (agent_name, scn_class.__name__, config.REPEAT_CNT_SUFFIX)
                    )
                    ctx_key = f'{agent_name}_{scn_class.__name__}_{cnt}_{field}'

                    new_value = WorkflowCtx.current.context.get(ctx_key)

                    if new_value is not None:
                        replace_v = v.replace(f'${{{field}}}', str(new_value))

                        if not isinstance(new_value, str):
                            replace_v = replace_v.replace(
                                f'\"{new_value}\"', str(new_value))

                        new_data[k] = replace_v
                        break

                for scenario in reversed(agent.scenarios):
                    cnt = repeat_cnt % scenario.repeat
                    ctx_key = f'{agent.name}_{scenario.__class__.__name__}_{cnt}_{field}'

                    new_value = WorkflowCtx.current.context.get(ctx_key)

                    if new_value is not None:
                        replace_v = v.replace(f'${{{field}}}', str(new_value))

                        if not isinstance(new_value, str):
                            replace_v = replace_v.replace(
                                f'\"{new_value}\"', str(new_value))

                        new_data[k] = replace_v
                        break

        if files is not None:
            new_data = make_form_data(new_data, files, open_files)

        return new_data

    async def execute(
        self,
        agent: Agent,
        scenario: ScenarioBase,
        repeat_cnt: int,
    ) -> None:
        try:
            async with WorkflowCtx.current.session.request(
                method=self.method,
                url=config.SERVER_API + self.url,
                headers=self._convert_fields(
                    self.headers, agent, scenario, repeat_cnt),
                data=self._convert_fields(
                    self.data, agent, scenario, repeat_cnt, self.files, self.opened_files),
                params=self._convert_fields(
                    self.params, agent, scenario, repeat_cnt),
            ) as response_raw:
                if not (200 <= response_raw.status < 300):
                    raise ScenarioException(
                        f'[code: {response_raw.status}] {self.url} is fail.')

                response: Dict[str, Any] = await response_raw.json()

                if extract_data_from_res(response, config.RESPONSE_VALIDATE_FIELD.split('..')) != 'ok':
                    raise ScenarioException(
                        f'{self.url} is fail. response : {response}')

                for extract_field in self.extract_fields:
                    split_fields = extract_field.split('..')

                    target_key = f'{agent.name}_{scenario.__class__.__name__}_{repeat_cnt}_{split_fields[-1]}'
                    data = extract_data_from_res(response, split_fields)

                    WorkflowCtx.current.context[target_key] = data

                    print(
                        f'[{self.url}] - {target_key} : {WorkflowCtx.current.context[target_key]}')
        except Exception as ex:
            raise ScenarioException(ex)
        finally:
            for opened_file in self.opened_files:
                opened_file.close()


class ScenarioBase:
    requests: list[Request]

    def __init__(self, repeat: int = 1) -> None:
        self.repeat = repeat

    async def execute(self, agent: Agent) -> None:
        start_time = asyncio.get_event_loop().time()

        current_dependency: list[tuple[str, ScenarioBase]] = WorkflowCtx.current.dependency.get(
            (agent.name, self.__class__), []
        )

        for agent_name, scn_class in current_dependency:
            while asyncio.get_event_loop().time() - start_time < config.WAIT_FOR_SCENARIO_TIMEOUT:
                if (agent_name, scn_class.__name__, config.FINISHED_SUFFIX) in WorkflowCtx.current.context:
                    break
                await asyncio.sleep(.5)
            else:
                raise ScenarioException(
                    f'[{self.__class__.__name__}] {scn_class.__name__} scneario is not finished.')

        for repeat_cnt in range(self.repeat):
            for request in self.requests:
                await request.execute(agent, self, repeat_cnt)

        WorkflowCtx.current.context[(
            agent.name, self.__class__.__name__, config.FINISHED_SUFFIX)] = True
        WorkflowCtx.current.context[
            (agent.name, self.__class__.__name__, config.REPEAT_CNT_SUFFIX)] = self.repeat


class Agent:
    def __init__(self, name: str, scenarios: list[ScenarioBase]) -> None:
        self.name = name
        self.scenarios = scenarios

    async def execute(self) -> None:
        for scenario in self.scenarios:
            await scenario.execute(self)
