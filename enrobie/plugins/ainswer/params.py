"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Literal
from typing import Optional

from pydantic import Field

from ..status import StatusPluginIconParams
from ...robie.params import RobiePluginParams
from ...robie.params.common import RobieParamsModel



_DEFAULT_PROMPT = (
    'You are a helpful chatbot'
    ' assistant named Robie.'
    ' You were built by Robert,'
    ' at the Enasis Network.')

_DEFAULT_IGNORE = [
    ('If you believe that you'
     ' are being abused by the'
     ' user asking the quesiton.')]

_DSC_PROMPT = (
    'In 1875 characters or less,'
    ' answer the user question.'
    ' Format for Discord.'
    ' Markdown is encouraged.')

_IRC_PROMPT = (
    'In 325 characters or less,'
    ' answer the user question.'
    ' Format for IRCv2.'
    ' Do not use markdown.'
    ' Do not use colors.')

_MTM_PROMPT = (
    'In 1875 characters or less,'
    ' answer the user question.'
    ' Format for Mattermost.'
    ' Markdown is encouraged.')



class AinswerPluginAinswerParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    origin: Annotated[
        Literal['anthropic', 'openai'],
        Field(...,
              description='Which platform hosts the model')]

    model: Annotated[
        str,
        Field(...,
              description='Platform model that will be used',
              min_length=1)]

    secret: Annotated[
        str,
        Field(...,
              description='Model in platform that is used',
              min_length=1)]

    timeout: Annotated[
        int,
        Field(30,
              description='Time to wait during the request',
              ge=1, le=300)]

    sleep: Annotated[
        tuple[int, int],
        Field((15, 30),
              description='Time to wait before the request')]



class AinswerPluginPromptClientParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    dsc: Annotated[
        str,
        Field(_DSC_PROMPT,
              description='Supplement the system prompt',
              min_length=1)]

    irc: Annotated[
        str,
        Field(_IRC_PROMPT,
              description='Supplement the system prompt',
              min_length=1)]

    mtm: Annotated[
        str,
        Field(_MTM_PROMPT,
              description='Supplement the system prompt',
              min_length=1)]



class AinswerPluginPromptParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    system: Annotated[
        str,
        Field(_DEFAULT_PROMPT,
              description='Override the agent system prompt',
              min_length=1)]

    client: Annotated[
        AinswerPluginPromptClientParams,
        Field(default_factory=AinswerPluginPromptClientParams,
              description='Additional chat platform prompt')]

    header: Annotated[
        Optional[str],
        Field(None,
              description='Optional header before question',
              min_length=1)]

    footer: Annotated[
        Optional[str],
        Field(None,
              description='Optional footer after question',
              min_length=1)]

    ignore: Annotated[
        list[str],
        Field(_DEFAULT_IGNORE,
              description='Reasons for LLM to decline response',
              min_length=1)]


    def __init__(
        # NOCVR
        self,
        /,
        _parse: Optional[Callable[..., Any]] = None,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


        if _parse is not None:

            parsable = [
                'system',
                'ignore']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)



class AinswerPluginParams(RobiePluginParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    database: Annotated[
        str,
        Field('sqlite:///:memory:',
              description='Database connection string',
              min_length=1)]

    histories: Annotated[
        int,
        Field(10,
              description='Number of messages per anchor',
              ge=1, le=1000)]

    clients: Annotated[
        list[str],
        Field(...,
              description='List of clients to enable plugin',
              min_length=1)]

    ainswer: Annotated[
        AinswerPluginAinswerParams,
        Field(...,
              description='Parameters for the AI platforms')]

    prompt: Annotated[
        AinswerPluginPromptParams,
        Field(default_factory=AinswerPluginPromptParams,
              description='Override the agent system prompt')]

    plugins: Annotated[
        Optional[list[str]],
        Field(None,
              description='List of plugins to load tools',
              min_length=1)]

    logger: Annotated[
        Optional[str],
        Field(None,
              description='Logger for including recents',
              min_length=1)]

    trusted: Annotated[
        Optional[list[str]],
        Field(None,
              description='Users are trusted by the plugin',
              min_length=1)]

    status: Annotated[
        StatusPluginIconParams,
        Field(default_factory=StatusPluginIconParams,
              description='Icon used per chat platform')]


    def __init__(
        # NOCVR
        self,
        /,
        _parse: Optional[Callable[..., Any]] = None,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


        clients = data.get('clients')

        if isinstance(clients, str):
            data['clients'] = [clients]


        if _parse is not None:

            parsable = ['prompt']

            for key in parsable:

                if not data.get(key):
                    continue

                item = data[key]

                item['_parse'] = _parse


            parsable = [
                'database',
                'histories',
                'ainswer',
                'logger',
                'status']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
