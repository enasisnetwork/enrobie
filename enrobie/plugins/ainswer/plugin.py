"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from pydantic_ai import Agent
from pydantic_ai.models import Model
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIModel

from .history import AinswerHistory
from .params import AinswerPluginParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...robie.threads import RobieThread



class AinswerPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin allows for interacting with an LLM model.
    """

    __history: AinswerHistory
    __model: Model
    __agent: Agent


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params = self.params

        prompt = params.prompt
        ainswer = params.ainswer
        secret = ainswer.secret
        origin = ainswer.origin

        system = prompt.system


        self.__history = (
            AinswerHistory(self))


        model: Model | None = None

        if origin == 'anthropic':
            model = AnthropicModel(
                ainswer.model,
                api_key=secret)

        elif origin == 'openai':
            model = OpenAIModel(
                ainswer.model,
                api_key=secret)

        assert model is not None, (
            'Model not instantiated')

        self.__model = model



        self.__agent = Agent(
            self.__model,
            system_prompt=system)


        self.__status('normal')


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        # Review the parameters


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
    ) -> Agent:
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
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        mqueue = thread.mqueue

        while not mqueue.empty:
            mqueue.get()

        # Put in ainswer method
        self.__status('normal')


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
            return None

        plugin = plugins['status']

        assert isinstance(
            plugin, StatusPlugin)

        (plugin.update(
            unique=self.name,
            group='Extensions',
            title='Chatting',
            icon=params.status,
            state=status))
