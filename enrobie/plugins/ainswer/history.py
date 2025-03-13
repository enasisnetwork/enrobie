"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Lock
from typing import Annotated
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.types import BaseModel
from encommon.types import DictStrAny
from encommon.types import NCNone

from pydantic import Field

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from .plugin import AinswerPlugin
    from ...robie.models import RobieMessage



AinswerHistoryKinds = Literal[
    'privmsg', 'chanmsg']



class SQLBase(DeclarativeBase):
    """
    Some additional class that SQLAlchemy requires to work.
    """



class AinswerHistoryTable(SQLBase):
    """
    Schematic for the database operations using SQLAlchemy.

    .. note::
       Fields are not completely documented for this model.
    """

    plugin = Column(
        String,
        primary_key=True,
        nullable=False)

    client = Column(
        String,
        primary_key=True,
        nullable=False)

    person = Column(
        String,
        primary_key=True,
        nullable=True)

    kind = Column(
        String,
        primary_key=True,
        nullable=False)

    author = Column(
        String,
        primary_key=True,
        nullable=False)

    anchor = Column(
        String,
        primary_key=True,
        nullable=False)

    message = Column(
        String,
        nullable=False)

    ainswer = Column(
        String,
        nullable=False)

    create = Column(
        Float,
        primary_key=True,
        nullable=False)

    __tablename__ = 'ainswer'



class AinswerHistoryRecord(BaseModel, extra='forbid'):
    """
    Contain the information regarding the chatting history.

    :param record: Record from the SQLAlchemy query routine.
    :param kwargs: Keyword arguments passed for downstream.
    """

    plugin: Annotated[
        str,
        Field(...,
              description='Plugin name where originated',
              min_length=1)]

    client: Annotated[
        str,
        Field(...,
              description='Client name where originated',
              min_length=1)]

    person: Annotated[
        Optional[str],
        Field(None,
              description='Person that author is matched',
              min_length=1)]

    kind: Annotated[
        AinswerHistoryKinds,
        Field(...,
              description='What kind of original message',
              min_length=1)]

    author: Annotated[
        str,
        Field(...,
              description='Nickname of message author',
              min_length=1)]

    anchor: Annotated[
        str,
        Field(None,
              description='Channel or private context',
              min_length=1)]

    message: Annotated[
        str,
        Field(...,
              description='Historical interaction content')]

    ainswer: Annotated[
        str,
        Field(...,
              description='Historical interaction content')]

    create: Annotated[
        str,
        Field(...,
              description='When the record was created',
              min_length=20,
              max_length=32)]


    def __init__(
        self,
        record: Optional[AinswerHistoryTable] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params: DictStrAny

        fields = [
            'plugin',
            'client',
            'person',
            'kind',
            'author',
            'anchor',
            'message',
            'ainswer',
            'create']


        if record is not None:

            params = {
                x: getattr(record, x)
                for x in fields}


        elif record is None:

            params = {
                x: kwargs.get(x)
                for x in fields}


        else:  # NOCVR
            raise ValueError('record')


        create = params['create']

        params['create'] = (
            str(Time(create)))


        super().__init__(**params)



class AinswerHistory:
    """
    Store the historical information for chat interactions.

    :param plugin: Plugin class instance for Chatting Robie.
    """

    __plugin: 'AinswerPlugin'

    __connect: str
    __locker: Lock

    __sengine: Engine
    __session: (
        # pylint: disable=unsubscriptable-object
        sessionmaker[Session])


    def __init__(
        self,
        plugin: 'AinswerPlugin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__plugin = plugin

        params = plugin.params

        self.__connect = (
            params.database)

        self.__locker = Lock()

        self.__build_engine()


    def __build_engine(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        path = self.__connect

        sengine = (
            create_engine(path))

        (SQLBase.metadata
         .create_all(sengine))

        session = (
            sessionmaker(sengine))

        self.__sengine = sengine
        self.__session = session


    def insert(  # noqa: CFQ002
        self,
        *,
        client: str,
        person: str | None,
        kind: str,
        author: str,
        anchor: str,
        message: str,
        ainswer: str,
    ) -> None:
        """
        Insert the record into the historical chat interactions.
        """

        plugin = self.__plugin

        sess = self.__session()
        lock = self.__locker

        table = AinswerHistoryTable
        model = AinswerHistoryRecord


        inputs: DictStrAny = {
            'plugin': plugin.name,
            'client': client,
            'person': person,
            'kind': kind,
            'author': author,
            'anchor': anchor,
            'message': message,
            'ainswer': ainswer,
            'create': float(Time())}

        record = model(**inputs)

        insert = record.endumped


        create = insert['create']

        insert['create'] = (
            float(Time(create)))


        with lock, sess as session:

            session.merge(
                table(**insert))

            session.commit()


        self.expunge(
            client=record.client,
            kind=record.kind,
            anchor=record.anchor)


    def process(
        self,
        mitem: 'RobieMessage',
        ainswer: str,
    ) -> None:
        """
        Insert the record into the historical chat interactions.

        :param mitem: Item containing information for operation.
        :param ainswer: Response from LLM relevant to question.
        """

        plugin = self.__plugin
        robie = plugin.robie
        childs = robie.childs
        persons = childs.persons
        clients = childs.clients

        assert mitem.author
        assert mitem.anchor
        assert mitem.message

        _person = mitem.person
        _kind = mitem.kind
        _author = mitem.author
        _anchor = mitem.anchor
        _message = mitem.message

        client = clients[
            mitem.client]

        person = (
            persons[_person]
            if _person is not None
            else None)

        self.insert(
            client=client.name,
            person=(
                person.name
                if person is not None
                else None),
            kind=_kind,
            author=_author[1],
            anchor=_anchor,
            message=_message,
            ainswer=ainswer)


    def expunge(
        self,
        *,
        client: Optional[str] = None,
        kind: Optional[str] = None,
        anchor: Optional[str] = None,
    ) -> None:
        """
        Remove the expired historical chat interaction records.
        """

        plugin = self.__plugin
        params = plugin.params

        maximum = params.histories


        sess = self.__session()
        lock = self.__locker

        table = AinswerHistoryTable

        _plugin = table.plugin
        _client = table.client
        _kind = table.kind
        _anchor = table.anchor
        _create = table.create


        with lock, sess as session:

            total = (
                session.query(table)
                .filter(
                    _plugin == plugin.name,
                    _client == client,
                    _kind == kind,
                    _anchor == anchor)
                .count())

            if total <= maximum:
                return

            cutoff = (
                session.query(_create)
                .filter(
                    _plugin == plugin.name,
                    _client == client,
                    _kind == kind,
                    _anchor == anchor)
                .order_by(_create.desc())
                .offset(maximum - 1)
                .limit(1).scalar())

            if cutoff is None:
                return NCNone

            (session.query(table)
             .filter(
                 _plugin == plugin.name,
                 _client == client,
                 _kind == kind,
                 _anchor == anchor,
                 _create < cutoff)
             .delete(synchronize_session=False))

            session.commit()


    def records(
        self,
        mitem: 'RobieMessage',
        limit: Optional[int] = None,
    ) -> list[AinswerHistoryRecord]:
        """
        Return all historical records for the chat interactions.

        :param mitem: Item containing information for operation.
        :param limit: Optionally restrict the records returned.
        :returns: Historical records for the chat interactions.
        """

        plugin = self.__plugin
        robie = plugin.robie
        childs = robie.childs
        clients = childs.clients

        assert mitem.author

        client = clients[
            mitem.client]


        return self.search(
            limit=limit,
            client=client.name,
            kind=mitem.kind,
            anchor=mitem.anchor)


    def search(  # noqa: CFQ002
        self,
        limit: Optional[int] = None,
        *,
        client: Optional[str] = None,
        person: Optional[str] = None,
        kind: Optional[str] = None,
        author: Optional[str] = None,
        anchor: Optional[str] = None,
    ) -> list[AinswerHistoryRecord]:
        """
        Return all historical records for the chat interactions.

        :param limit: Optionally restrict the records returned.
        :returns: Historical records for the chat interactions.
        """

        plugin = self.__plugin


        sess = self.__session()
        lock = self.__locker

        records: list[AinswerHistoryRecord]

        table = AinswerHistoryTable
        model = AinswerHistoryRecord

        _plugin = table.plugin
        _client = table.client
        _person = table.person
        _kind = table.kind
        _author = table.author
        _anchor = table.anchor
        _create = table.create


        with lock, sess as session:

            records = []

            query = (
                session.query(table)
                .filter(
                    _plugin == plugin.name)
                .order_by(_create.desc()))

            if client is not None:
                query = query.filter(
                    _client == client)

            if person is not NCNone:
                query = query.filter(
                    _person == person)

            if kind is not None:
                query = query.filter(
                    _kind == kind)

            if author is not None:
                query = query.filter(
                    _author == author)

            if anchor is not None:
                query = query.filter(
                    _anchor == anchor)

            if limit is not None:
                query = query.limit(limit)


            for record in query.all():

                object = model(record)

                records.append(object)

            return records[::-1]
