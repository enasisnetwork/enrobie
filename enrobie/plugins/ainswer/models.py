"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import Type

from httpx import AsyncClient

if TYPE_CHECKING:
    from pydantic_ai import Agent
    from pydantic_ai.models.anthropic import AnthropicModel
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.settings import ModelSettings

    from .common import AinswerDepends
    from .plugin import AinswerPlugin



class AinswerModels:
    """
    Return the class object that was imported within method.

    :param plugin: Plugin class instance for Chatting Robie.
    """

    __plugin: 'AinswerPlugin'


    def __init__(
        self,
        plugin: 'AinswerPlugin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__plugin = plugin


    @classmethod
    def agent(
        cls,
    ) -> Type['Agent[AinswerDepends, str]']:
        """
        Return the class object that was imported within method.
        """

        from pydantic_ai import Agent

        return Agent


    @classmethod
    def settings(
        cls,
    ) -> Type['ModelSettings']:
        """
        Return the class object that was imported within method.
        """

        from pydantic_ai.settings import ModelSettings

        return ModelSettings


    @property
    def anthropic(
        self,
    ) -> 'AnthropicModel':
        """
        Return the class object that was imported within method.
        """

        from pydantic_ai.models.anthropic import AnthropicModel
        from pydantic_ai.providers.anthropic import AnthropicProvider

        plugin = self.__plugin

        params = plugin.params
        ainswer = params.ainswer
        secret = ainswer.secret

        provider = (
            AnthropicProvider(
                api_key=secret))

        return AnthropicModel(
            ainswer.model,
            provider=provider)


    @property
    def openai(
        self,
    ) -> 'OpenAIChatModel':
        """
        Return the class object that was imported within method.
        """

        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.openai import OpenAIProvider

        plugin = self.__plugin

        params = plugin.params
        ainswer = params.ainswer
        secret = ainswer.secret

        provider = (
            OpenAIProvider(
                api_key=secret))

        return OpenAIChatModel(
            ainswer.model,
            provider=provider)


    @property
    def ollama(
        self,
    ) -> 'OpenAIChatModel':
        """
        Return the class object that was imported within method.
        """

        from openai import AsyncOpenAI
        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.ollama import OllamaProvider

        plugin = self.__plugin

        params = plugin.params
        ainswer = params.ainswer
        baseurl = ainswer.baseurl
        secret = ainswer.secret

        client_async = (
            AsyncClient(
                timeout=300))

        client = AsyncOpenAI(
            base_url=baseurl,
            api_key=secret,
            timeout=300,
            http_client=client_async)

        provider = (
            OllamaProvider(
                openai_client=client))

        return OpenAIChatModel(
            ainswer.model,
            provider=provider)
