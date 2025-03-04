"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Lock
from typing import Annotated
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.types import BaseModel
from encommon.types import DictStrAny

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
    from ...robie.childs import RobieClient



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
            'author',
            'anchor',
            'message',
            'ainswer',
            'create']


        if record is not None:

            params = {
                x: getattr(record, x)
                for x in fields}


        elif kwargs is not None:

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


    def insert(
        self,
        client: 'RobieClient',
        author: str,
        anchor: str,
        message: str,
        ainswer: str,
    ) -> None:
        """
        Insert the record into the historical chat interactions.

        :param client: Client class instance for Chatting Robie.
        :param author: Name of the user that submitted question.
        :param anchor: Channel name or other context or thread.
        :param message: Question that will be asked of the LLM.
        :param ainswer: Response from LLM relevant to question.
        """

        plugin = self.__plugin

        sess = self.__session()
        lock = self.__locker

        table = AinswerHistoryTable
        model = AinswerHistoryRecord


        inputs: DictStrAny = {
            'plugin': plugin.name,
            'client': client.name,
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


        self.expunge(client, anchor)


    def expunge(
        self,
        client: 'RobieClient',
        anchor: str,
    ) -> None:
        """
        Remove the expired historical chat interaction records.

        :param client: Client class instance for Chatting Robie.
        :param anchor: Channel name or other context or thread.
        """

        plugin = self.__plugin

        sess = self.__session()
        lock = self.__locker

        table = AinswerHistoryTable

        _plugin = table.plugin
        _client = table.client
        _anchor = table.anchor
        _create = table.create


        with lock, sess as session:

            query = (
                session.query(table)
                .filter(
                    _plugin == plugin.name,
                    _client == client.name,
                    _anchor == anchor)
                .order_by(_create.desc())
                .distinct())

            delete = query.all()[10:]

            for record in delete:
                session.delete(record)

            session.commit()


    def records(
        self,
        client: 'RobieClient',
        anchor: str,
    ) -> list[AinswerHistoryRecord]:
        """
        Return all historical records for the chat interactions.

        :param client: Client class instance for Chatting Robie.
        :param anchor: Channel name or other context or thread.
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
        _anchor = table.anchor
        _create = table.create


        with lock, sess as session:

            records = []

            query = (
                session.query(table)
                .filter(
                    _plugin == plugin.name,
                    _client == client.name,
                    _anchor == anchor)
                .order_by(_create.asc()))


            for record in query.all():

                object = model(record)

                records.append(object)

            return records
