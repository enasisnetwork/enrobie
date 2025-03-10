"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from random import randint
from time import sleep as block_sleep
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import NCNone

from .helpers import composedsc
from .helpers import composeirc
from .helpers import composemtm
from .helpers import engagellm
from .helpers import promptllm
from .history import AinswerHistory
from .models import AinswerResponse
from .params import AinswerPluginParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from pydantic_ai import Agent
    from pydantic_ai.models import Model
    from ...robie.threads import RobieThread
    from ...robie.childs import RobieClient
    from ...robie.models import RobieMessage



class AinswerPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin allows for interacting with an LLM model.
    """

    __started: bool

    __history: AinswerHistory

    __model: 'Model'
    __agent: 'Agent'


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        from pydantic_ai import Agent
        from pydantic_ai.settings import ModelSettings


        self.__started = False

        params = self.params

        prompt = params.prompt
        ainswer = params.ainswer
        secret = ainswer.secret
        origin = ainswer.origin

        system = prompt.system


        self.__history = (
            AinswerHistory(self))


        model: 'Model' | None = None

        if origin == 'anthropic':

            from pydantic_ai.models import anthropic

            _anthropic = (
                anthropic.AnthropicModel)

            model = _anthropic(
                ainswer.model,
                api_key=secret)

        elif origin == 'openai':

            from pydantic_ai.models import openai

            _openai = (
                openai.OpenAIModel)

            model = _openai(
                ainswer.model,
                api_key=secret)

        assert model is not None, (
            'Model not instantiated')

        self.__model = model


        settings = ModelSettings(
            timeout=ainswer.timeout)

        self.__agent = Agent(
            self.__model,
            model_settings=settings,
            system_prompt=system)

        self.__status('pending')


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        # Review the parameters


    @classmethod
    def schema(
        cls,
    ) -> Type[AinswerPluginParams]:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        return AinswerPluginParams


    @property
    def params(
        self,
    ) -> AinswerPluginParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        params = super().params

        assert isinstance(
            params,
            AinswerPluginParams)

        return params


    @property
    def history(
        self,
    ) -> AinswerHistory:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__history


    @property
    def agent(
        self,
    ) -> 'Agent':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__agent


    def operate(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Robie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        mqueue = thread.mqueue
        member = thread.member
        cqueue = member.cqueue

        names = (
            self.params.clients)

        if not self.__started:
            self.__started = True
            self.__status('normal')


        while not mqueue.empty:

            mitem = mqueue.get()

            name = mitem.client
            time = mitem.time
            isme = mitem.isme
            family = mitem.family

            if name not in names:
                continue  # NOCVR

            if isme is True:
                continue

            if time.since > 15:
                continue  # NOCVR

            if family == 'discord':
                composedsc(
                    self, cqueue, mitem)

            if family == 'irc':
                composeirc(
                    self, cqueue, mitem)

            if family == 'mattermost':
                composemtm(
                    self, cqueue, mitem)


    def ainswer(  # noqa: CFQ001,CFQ002
        self,
        client: 'RobieClient',
        prompt: str,
        respond: Type[AinswerResponse],
        *,
        whoami: Optional[str] = None,
        author: Optional[str] = None,
        anchor: Optional[str] = None,
        message: Optional[str] = None,
        mitem: Optional['RobieMessage'] = None,
    ) -> str:
        """
        Submit the question to the LLM and return the response.

        :param client: Client class instance for Chatting Robie.
        :param prompt: Additional prompt insert before question.
        :param respond: Model to describe the expected response.
        :param whoami: What is my current nickname on platform.
        :param author: Name of the user that submitted question.
        :param anchor: Channel name or other context or thread.
        :param message: Question that will be asked of the LLM.
        :param mitem: Item containing information for operation.
        :returns: Response adhering to provided specifications.
        """

        robie = self.robie
        config = robie.config
        sargs = config.sargs
        history = self.history
        params = self.params

        _whoami: Optional[str] = None
        _author: Optional[str] = None


        # Also in promptllm helper
        if mitem is not None:

            if mitem.whome is not None:

                whoami = (
                    mitem.whome[0]
                    if whoami is None
                    else whoami)

                _whoami = mitem.whome[1]

                _whoami = (
                    _whoami
                    if _whoami != whoami
                    else None)


            if mitem.author is not None:

                author = (
                    mitem.author[0]
                    if author is None
                    else author)

                _author = mitem.author[1]

                _author = (
                    _author
                    if _author != author
                    else None)


            anchor = (
                mitem.anchor
                if anchor is None
                else anchor)

            message = (
                mitem.message
                if message is None
                else message)


        assert whoami is not None
        assert author is not None
        assert anchor is not None
        assert message is not None


        robie.logger.log_i(
            base=self,
            name=self,
            item='ainswer',
            client=client.name,
            author=author,
            anchor=anchor,
            message=message)


        sleep = (
            params.ainswer.sleep)

        system = (
            params.prompt.system)

        header = (
            params.prompt.header)

        footer = (
            params.prompt.footer)

        ignore = (
            params.prompt.ignore)


        imsorry = (
            f"I'm sorry {author}, I'm"
            " afraid I can't do that.")


        _sleep = randint(*sleep)

        robie.logger.log_i(
            base=self,
            name=self,
            item='ainswer',
            client=client.name,
            author=author,
            anchor=anchor,
            status='pausing',
            seconds=_sleep)

        # Useful to prevent abuse but
        # also reduce immediate reply
        # and allow for plugin events
        # before Jinja2 referencing
        block_sleep(_sleep)


        try:

            prompt = promptllm(
                self, client,
                prompt=prompt,
                whoami=whoami,
                whoami_uniq=_whoami,
                author=author,
                author_uniq=_author,
                anchor=anchor,
                message=message,
                header=header,
                footer=footer,
                ignore=ignore,
                mitem=mitem)

            if sargs.get('console'):
                robie.printer({
                    'system': system,
                    'prompt': prompt,
                    'sleep': _sleep})

            response = engagellm(
                self, prompt, respond)

            ainswer = response.text

            self.__status('normal')

            robie.logger.log_i(
                base=self,
                name=self,
                item='ainswer',
                client=client.name,
                author=author,
                anchor=anchor,
                ainswer=ainswer)

            history.insert(
                client,
                author, anchor,
                message, ainswer)

            return ainswer


        except Exception as reason:

            self.__status('failure')

            robie.logger.log_e(
                base=self,
                name=self,
                item='ainswer',
                client=client.name,
                author=author,
                anchor=anchor,
                status='exception',
                exc_info=reason)

            return imsorry


    def __status(
        self,
        status: StatusPluginStates,
    ) -> None:
        """
        Update or insert the status of the Robie child instance.

        :param status: One of several possible value for status.
        """

        robie = self.robie
        childs = robie.childs
        plugins = childs.plugins
        params = self.params

        if 'status' not in plugins:
            return NCNone

        plugin = plugins['status']

        assert isinstance(
            plugin, StatusPlugin)

        (plugin.update(
            unique=self.name,
            group='Extensions',
            title='Ainswer',
            icon=params.status,
            state=status))
