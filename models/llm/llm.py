from collections.abc import Generator
from typing import Optional, Union

from dify_plugin import OAICompatLargeLanguageModel
from dify_plugin.entities.model import (
    AIModelEntity,
    FetchFrom,
    I18nObject,
    ModelFeature,
    ModelPropertyKey,
    ModelType,
    ParameterRule,
    ParameterType,
)
from dify_plugin.entities.model.llm import LLMMode, LLMResult
from dify_plugin.entities.model.message import PromptMessage, PromptMessageTool

EMPIRIOLABS_API_BASE = "https://api.empiriolabs.ai/v1"


class EmpirioLabsLargeLanguageModel(OAICompatLargeLanguageModel):
    def _invoke(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        model_parameters: dict,
        tools: Optional[list[PromptMessageTool]] = None,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[LLMResult, Generator]:
        self._add_custom_parameters(credentials)
        self._add_function_call(model, credentials)
        return super()._invoke(
            model, credentials, prompt_messages, model_parameters, tools, stop, stream, user
        )

    def validate_credentials(self, model: str, credentials: dict) -> None:
        self._add_custom_parameters(credentials)
        super().validate_credentials(model, credentials)

    def get_num_tokens(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        tools: Optional[list[PromptMessageTool]] = None,
    ) -> int:
        self._add_custom_parameters(credentials)
        return super().get_num_tokens(model, credentials, prompt_messages, tools)

    @staticmethod
    def _add_custom_parameters(credentials: dict) -> None:
        credentials["endpoint_url"] = EMPIRIOLABS_API_BASE
        credentials["mode"] = LLMMode.CHAT.value

    def _add_function_call(self, model: str, credentials: dict) -> None:
        model_schema = self.get_model_schema(model, credentials)
        if model_schema and {
            ModelFeature.TOOL_CALL,
            ModelFeature.MULTI_TOOL_CALL,
        }.intersection(model_schema.features or []):
            credentials["function_calling_type"] = "tool_call"

    def get_customizable_model_schema(
        self,
        model: str,
        credentials: dict,
    ) -> Optional[AIModelEntity]:
        features = []
        if credentials.get("function_calling_type") == "tool_call":
            features = [
                ModelFeature.TOOL_CALL,
                ModelFeature.MULTI_TOOL_CALL,
                ModelFeature.STREAM_TOOL_CALL,
            ]
        if credentials.get("vision_support") == "support":
            features.append(ModelFeature.VISION)

        return AIModelEntity(
            model=model,
            label=I18nObject(en_us=model, zh_hans=model),
            model_type=ModelType.LLM,
            features=features,
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                ModelPropertyKey.CONTEXT_SIZE: int(credentials.get("context_size", 128000)),
                ModelPropertyKey.MODE: LLMMode.CHAT.value,
            },
            parameter_rules=[
                ParameterRule(
                    name="temperature",
                    use_template="temperature",
                    label=I18nObject(en_us="Temperature", zh_hans="Temperature"),
                    type=ParameterType.FLOAT,
                ),
                ParameterRule(
                    name="max_tokens",
                    use_template="max_tokens",
                    default=4096,
                    min=1,
                    max=int(credentials.get("max_tokens", 8192)),
                    label=I18nObject(en_us="Max Tokens", zh_hans="Max Tokens"),
                    type=ParameterType.INT,
                ),
                ParameterRule(
                    name="top_p",
                    use_template="top_p",
                    label=I18nObject(en_us="Top P", zh_hans="Top P"),
                    type=ParameterType.FLOAT,
                ),
                ParameterRule(
                    name="frequency_penalty",
                    use_template="frequency_penalty",
                    label=I18nObject(en_us="Frequency Penalty", zh_hans="Frequency Penalty"),
                    type=ParameterType.FLOAT,
                ),
                ParameterRule(
                    name="presence_penalty",
                    use_template="presence_penalty",
                    label=I18nObject(en_us="Presence Penalty", zh_hans="Presence Penalty"),
                    type=ParameterType.FLOAT,
                ),
            ],
        )
