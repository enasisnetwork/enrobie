"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from json import dumps
from typing import Any
from typing import Callable
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.times import Time
from encommon.types import DictStrAny
from encommon.types.strings import COMMAS
from encommon.types.strings import NEWLINE
from encommon.types.strings import SEMPTY

from .common import AinswerResponse

if TYPE_CHECKING:
    from .plugin import AinswerPlugin
    from ...robie.childs import RobieClient
    from ...robie.childs import RobiePerson
    from ...robie.models import RobieMessage



AinswerIgnored = 'no_response'

AinswerTool = Callable[..., Any]



@dataclass
class AinswerDepends:
    """
    Dependencies related to operation with PydanticAI tools.
    """

    plugin: 'AinswerPlugin'
    mitem: Optional['RobieMessage']



class AinswerToolset:
    """
    Enumerate the plugins and return those that are related.

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


    @property
    def toolset(
        self,
    ) -> list[AinswerTool]:
        """
        Return the related tools that were found in the plugins.

        :returns: Related tools that were found in the plugins.
        """

        from .plugin import AinswerPlugin

        plugin = self.__plugin

        toolset: list[AinswerTool] = []

        if not plugin.thread:
            return toolset

        assert plugin.thread

        thread = plugin.thread
        params = plugin.params

        names = params.plugins

        if names is None:
            return toolset


        plugins = (
            thread.service
            .plugins.childs
            .values())

        for helper in plugins:

            name = helper.name

            if name not in names:
                continue

            ignored = isinstance(
                helper, AinswerPlugin)

            if ignored is True:
                continue

            related = hasattr(
                helper, 'ainswer')

            if related is False:
                continue

            assert hasattr(
                helper, 'ainswer')

            toolset.extend(
                helper.ainswer())


        return toolset



class AinswerQuestion:
    """
    Construct prompt and allow for interacting with the LLM.

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


    def prompt(
        self,
        mitem: 'RobieMessage',
        prompt: str,
    ) -> str:
        """
        Return the message prefixed with runtime prompt values.

        :param mitem: Item containing information for operation.
        :param prompt: Additional prompt insert before question.
        :returns: Message prefixed with runtime prompt values.
        """

        plugin = self.__plugin
        robie = plugin.robie
        params = plugin.params

        _prompt = params.prompt

        header = _prompt.header
        footer = _prompt.footer

        assert mitem.whome

        person = self.__person(mitem)
        client = self.__client(mitem)
        family = mitem.family
        kind = mitem.kind
        whome = mitem.whome


        parsed = robie.j2parse(
            {'prompt': prompt,
             'header': header,
             'footer': footer},
            {'plugin': plugin,
             'client': client,
             'person': person,
             'family': family,
             'kind': kind,
             'whoami': whome[0],
             'mitem': mitem})

        prompt = parsed['prompt']
        header = parsed['header']
        footer = parsed['footer']


        history = (
            self.prompt_history(
                mitem, prompt))

        ignored = (
            self.prompt_ignored(
                mitem, prompt))

        metadata = (
            self.prompt_metadata(
                mitem, prompt))

        channel = (
            self.prompt_channel(
                mitem, prompt))

        recents = (
            self.prompt_recents(
                mitem, prompt))


        returned = SEMPTY.join([
            '**Instructions**\n',
            (f'{prompt}\n\n'
             if prompt
             else SEMPTY),
            (f'{history}\n\n'
             if history
             else SEMPTY),
            (f'{ignored}\n\n'
             if ignored
             else SEMPTY),
            (f'{metadata}\n\n'
             if metadata
             else SEMPTY),
            (f'{channel}\n\n'
             if channel
             else SEMPTY),
            (f'{recents}\n\n'
             if recents
             else SEMPTY),
            (f'{header}\n\n'
             if header is not None
             and len(header) >= 1
             else SEMPTY),
            ('**Question**\n'
             f'{mitem.message}'),
            (f'\n\n{footer}'
             if footer is not None
             and len(footer) >= 1
             else SEMPTY)])


        return returned.strip()


    def prompt_history(
        self,
        mitem: 'RobieMessage',
        prompt: str,
    ) -> str:
        """
        Return the message prefixed with runtime prompt values.

        :param mitem: Item containing information for operation.
        :param prompt: Additional prompt insert before question.
        :returns: Message prefixed with runtime prompt values.
        """

        plugin = self.__plugin
        history = plugin.history

        items: list[DictStrAny] = []

        records = (
            history.records(mitem))

        for record in records:

            person = record.person
            author = record.author
            message = record.message
            ainswer = record.ainswer

            create = (
                Time(record.create)
                .simple)

            items.extend([
                {'role': 'user',
                 'content': message,
                 'nick': author,
                 'user': person,
                 'time': create},
                {'role': 'assistant',
                 'content': ainswer}])

        if len(items) == 0:
            return SEMPTY

        dumped = [
            dumps(x) for x in items]

        return (
            '**Previous Interactions**\n'
            'You have previously had the following'
            ' direct conversations within scope.\n'
            f'{NEWLINE.join(dumped)}')


    def prompt_ignored(
        self,
        mitem: 'RobieMessage',
        prompt: str,
    ) -> str:
        """
        Return the message prefixed with runtime prompt values.

        :param mitem: Item containing information for operation.
        :param prompt: Additional prompt insert before question.
        :returns: Message prefixed with runtime prompt values.
        """

        plugin = self.__plugin
        params = plugin.params

        _prompt = params.prompt
        ignore = _prompt.ignore

        response = AinswerIgnored
        delim = f'{NEWLINE} - '

        return (
            '**Responding**\n'
            'There are reasons not to respond to the'
            ' user question. If you think you should'
            f' not respond, reply with {response}.\n'
            f'Reasons to reply with only {response}'
            f' include:{delim}{delim.join(ignore)}')


    def prompt_metadata(
        self,
        mitem: 'RobieMessage',
        prompt: str,
    ) -> str:
        """
        Return the message prefixed with runtime prompt values.

        :param mitem: Item containing information for operation.
        :param prompt: Additional prompt insert before question.
        :returns: Message prefixed with runtime prompt values.
        """

        assert mitem.whome
        assert mitem.author

        person = self.__person(mitem)
        time = mitem.time
        family = mitem.family
        kind = mitem.kind
        whome = mitem.whome
        author = mitem.author

        returned = (
            '**Message Metadata**\n'
            f'Client family: {family}\n'
            f'Message kind: {kind}\n'
            f'Message time: {time}\n\n'
            '**User Metadata**\n'
            f'User nickname: {author[0]}\n'
            f'User serverID: {author[1]}\n')


        if person is not None:

            returned += (
                'Robie username: '
                f'{person.name}\n')

            _first = person.first
            _last = person.last
            _about = person.about

            if _first is not None:
                returned += (
                    f'First name: {_first}\n')

            if _last is not None:
                returned += (
                    f'Last name: {_last}\n')

            if _about is not None:
                returned += (
                    f'Description: {_about}\n')

        returned += (
            '\n**Additional Metadata**\n'
            f'Your nickname: {whome[0]}\n'
            f'Your serverID: {whome[1]}\n')

        return returned.strip()


    def prompt_channel(
        self,
        mitem: 'RobieMessage',
        prompt: str,
    ) -> str:
        """
        Return the message prefixed with runtime prompt values.

        :param mitem: Item containing information for operation.
        :param prompt: Additional prompt insert before question.
        :returns: Message prefixed with runtime prompt values.
        """

        assert mitem.anchor

        client = self.__client(mitem)
        kind = mitem.kind
        anchor = mitem.anchor

        if kind != 'chanmsg':
            return SEMPTY

        channel = (
            client.channels
            .select(anchor))

        if channel is None:
            return SEMPTY

        unique = channel.unique
        title = channel.title
        topic = channel.topic
        members = channel.members


        returned = (
            '**Channel Metadata**\n'
            f'Unique: {unique}\n')


        if title and title != anchor:
            returned += f'Title: {title}\n'

        if topic is not None:
            returned += f'Topic: {topic}\n'

        if members is not None:
            users = COMMAS.join(members)
            returned += f'Users: {users}\n'


        return returned.strip()


    def prompt_recents(  # noqa: CFQ004
        self,
        mitem: 'RobieMessage',
        prompt: str,
    ) -> str:
        """
        Return the message prefixed with runtime prompt values.

        :param mitem: Item containing information for operation.
        :param prompt: Additional prompt insert before question.
        :returns: Message prefixed with runtime prompt values.
        """

        from ..logger import LoggerPlugin

        plugin = self.__plugin
        robie = plugin.robie
        childs = robie.childs
        plugins = childs.plugins
        params = plugin.params

        name = params.logger
        limit = params.histories

        kind = mitem.kind

        if kind != 'chanmsg':
            return SEMPTY

        if name not in plugins:
            return SEMPTY  # NOCVR

        _plugin = plugins[name]

        if _plugin.name != name:
            return SEMPTY  # NOCVR

        assert isinstance(
            _plugin, LoggerPlugin)

        records = (
            _plugin.history
            .plaintext(limit, mitem))

        return (
            '**Channel Recents**\n'
            'These are the most recent messages from'
            ' the current channel or direct message.'
            ' When client family is IRC or Mattermost,'
            ' you do not see your messages below.\n'
            f'{NEWLINE.join(records)}')


    def __person(
        self,
        mitem: 'RobieMessage',
    ) -> Optional['RobiePerson']:
        """
        Return the person instance where the message originated.

        :param mitem: Item containing information for operation.
        :returns: Person instance where the message originated.
        """

        plugin = self.__plugin
        robie = plugin.robie
        childs = robie.childs
        persons = childs.persons

        _person = mitem.person

        if _person is None:
            return None

        return persons[_person]


    def __client(
        self,
        mitem: 'RobieMessage',
    ) -> 'RobieClient':
        """
        Return the client instance where the message originated.

        :param mitem: Item containing information for operation.
        :returns: Client instance where the message originated.
        """

        plugin = self.__plugin
        robie = plugin.robie
        childs = robie.childs
        clients = childs.clients

        _client = mitem.client

        return clients[_client]


    def submit(
        self,
        prompt: str,
        respond: Type[AinswerResponse],
        mitem: Optional['RobieMessage'] = None,
    ) -> AinswerResponse:
        """
        Submit the question to the LLM and return the response.

        :param prompt: Question that will be asked of the LLM.
        :param respond: Model to describe the expected response.
        :param mitem: Item containing information for operation.
        :returns: Response adhering to provided specifications.
        """

        plugin = self.__plugin

        agent = plugin.agent
        request = agent.run_sync
        model = AinswerDepends

        depends = model(
            plugin=plugin,
            mitem=mitem)

        runsync = request(
            user_prompt=prompt,
            result_type=respond,
            deps=depends)

        return runsync.data
