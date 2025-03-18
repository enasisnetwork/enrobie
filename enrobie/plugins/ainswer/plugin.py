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
from typing import Union

from encommon.types import DictStrAny
from encommon.types import NCNone

from .ainswer import AinswerDepends
from .ainswer import AinswerQuestion
from .ainswer import AinswerToolset
from .common import AinswerResponse
from .helpers import composedsc
from .helpers import composeirc
from .helpers import composemtm
from .history import AinswerHistory
from .params import AinswerPluginParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePerson
from ...robie.childs import RobiePlugin
from ...robie.models import RobieMessage

if TYPE_CHECKING:
    from pydantic_ai import Agent
    from pydantic_ai.models import Model



class AinswerPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin allows for interacting with an LLM model.
    """

    __started: bool

    __toolset: AinswerToolset
    __question: AinswerQuestion
    __history: AinswerHistory

    __model: 'Model'
    __agent: Optional['Agent[AinswerDepends, str]']


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__started = False

        params = self.params

        ainswer = params.ainswer
        secret = ainswer.secret
        origin = ainswer.origin


        self.__toolset = (
            AinswerToolset(self))

        self.__question = (
            AinswerQuestion(self))

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

        self.__agent = None


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
    def toolset(
        self,
    ) -> AinswerToolset:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__toolset


    @property
    def question(
        self,
    ) -> AinswerQuestion:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__question


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
    ) -> 'Agent[AinswerDepends, str]':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        from pydantic_ai import Agent
        from pydantic_ai.settings import ModelSettings

        agent = self.__agent

        if agent is not None:
            return agent

        params = self.params
        prompt = params.prompt
        ainswer = params.ainswer
        system = prompt.system

        toolset = (
            self.__toolset.toolset)

        settings = ModelSettings(
            timeout=ainswer.timeout)

        self.__agent = Agent(
            self.__model,
            system_prompt=system,
            model_settings=settings,
            deps_type=AinswerDepends,
            tools=toolset)

        return self.__agent


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.
        """

        assert self.thread

        thread = self.thread
        mqueue = thread.mqueue

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

            # Ignore unrelated clients
            if name not in names:
                continue  # NOCVR

            # Ignore event from client
            if isme is True:
                continue

            # Ignore expired messages
            if time.since > 15:
                continue  # NOCVR

            # Basic trust enforcement
            if self.notrust(mitem):
                continue


            if family == 'discord':
                composedsc(self, mitem)

            if family == 'irc':
                composeirc(self, mitem)

            if family == 'mattermost':
                composemtm(self, mitem)


    def ainswer(  # noqa: CFQ001
        self,
        mitem: 'RobieMessage',
        prompt: str,
        respond: Type[AinswerResponse],
    ) -> str:
        """
        Submit the question to the LLM and return the response.

        :param mitem: Item containing information for operation.
        :param prompt: Additional prompt insert before question.
        :param respond: Model to describe the expected response.
        :returns: Response adhering to provided specifications.
        """

        robie = self.robie
        config = robie.config
        childs = robie.childs
        persons = childs.persons
        clients = childs.clients
        sargs = config.sargs
        question = self.question
        history = self.history
        params = self.params

        _ainswer = params.ainswer
        _prompt = params.prompt

        sleep = _ainswer.sleep
        system = _prompt.system

        assert mitem.whome
        assert mitem.author
        assert mitem.anchor
        assert mitem.message

        _client = mitem.client
        _person = mitem.person
        author = mitem.author
        anchor = mitem.anchor
        message = mitem.message

        client = (
            clients[_client]
            if _client is not None
            else None)

        person = (
            persons[_person]
            if _person is not None
            else None)


        robie.logger.log_i(
            base=self,
            name=self,
            item='ainswer',
            client=client.name,
            person=(
                person.name
                if person is not None
                else None),
            author=author[0],
            anchor=anchor,
            message=message)


        imsorry = (
            f"I'm sorry {author[0]}, I'm"
            " afraid I can't do that.")


        _sleep = randint(*sleep)

        robie.logger.log_i(
            base=self,
            name=self,
            item='ainswer',
            client=client.name,
            person=(
                person.name
                if person is not None
                else None),
            author=author[0],
            anchor=anchor,
            status='pausing',
            seconds=_sleep)

        # Useful to prevent abuse but
        # also reduce immediate reply
        # and allow for plugin events
        # before Jinja2 referencing
        block_sleep(_sleep)


        try:

            prompt = (
                question.prompt(
                    mitem, prompt))

            if sargs.get('console'):
                robie.printer({
                    'system': system,
                    'prompt': prompt,
                    'sleep': _sleep})

            response = (
                question.submit(
                    prompt, respond,
                    mitem=mitem))

            ainswer = response.text

            self.__status('normal')

            robie.logger.log_i(
                base=self,
                name=self,
                item='ainswer',
                client=client.name,
                person=(
                    person.name
                    if person is not None
                    else None),
                author=author[0],
                anchor=anchor,
                ainswer=ainswer)

            history.process(
                mitem, ainswer)

            return ainswer


        except Exception as reason:

            self.__status('failure')

            robie.logger.log_e(
                base=self,
                name=self,
                item='ainswer',
                client=client.name,
                person=(
                    person.name
                    if person is not None
                    else None),
                author=author[0],
                anchor=anchor,
                status='exception',
                exc_info=reason)

            return imsorry


    def printer(
        self,
        source: DictStrAny,
        color: int = 6,
    ) -> None:
        """
        Print the contents for the object within Robie instance.

        :param source: Content which will be shown after header.
        :param color: Override the color used for box character.
        """

        robie = self.robie
        config = robie.config
        sargs = config.sargs

        if not sargs.get('console'):
            return None

        robie.printer(source, color)


    def trusted(
        self,
        check: Union[str, RobiePerson, RobieMessage],
    ) -> bool:
        """
        Return the boolean indicating whether person is trusted.

        :param check: Validate the person is trusted by plugin.
        :returns: Boolean indicating whether person is trusted.
        """

        params = self.params
        trusted = params.trusted

        if trusted is None:
            return True

        if isinstance(check, RobieMessage):

            if not check.person:
                return False

            check = check.person

        elif isinstance(check, RobiePerson):
            check = check.name

        return check in trusted


    def notrust(
        self,
        check: Union[str, RobiePerson, RobieMessage],
    ) -> bool:
        """
        Return the boolean indicating whether person is trusted.

        :param check: Validate the person is trusted by plugin.
        :returns: Boolean indicating whether person is trusted.
        """

        return not self.trusted(check)


    def __status(
        self,
        status: StatusPluginStates,
    ) -> None:
        """
        Update or insert the status of the Robie child instance.

        :param status: One of several possible value for status.
        """

        thread = self.thread
        params = self.params

        if thread is None:
            return None

        plugins = (
            thread.service
            .plugins.childs)

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
