"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from random import randint
from threading import Lock
from typing import Annotated
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.crypts import Hashes
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



AinswerMemoryKinds = Literal[
    'privmsg', 'chanmsg']

AinswerMemoryMessageField = Annotated[
    str,
    Field(...,
          description='Historical person memorable',
          min_length=1,
          max_length=400)]

AinswerMemoryUniqueField = Annotated[
    str,
    Field(...,
          description='Unique identifier for memory',
          min_length=36,
          max_length=36)]



class SQLBase(DeclarativeBase):
    """
    Some additional class that SQLAlchemy requires to work.
    """



class AinswerMemoryTable(SQLBase):
    """
    Schematic for the database operations using SQLAlchemy.

    .. note::
       Fields are not completely documented for this model.
    """

    plugin = Column(
        String,
        primary_key=True,
        nullable=False)

    person = Column(
        String,
        primary_key=True,
        nullable=False)

    unique = Column(
        String,
        primary_key=True,
        nullable=False)

    message = Column(
        String,
        nullable=False)

    create = Column(
        Float,
        primary_key=True,
        nullable=False)

    __tablename__ = 'ainswer_memory'



class AinswerMemoryRecord(BaseModel, extra='forbid'):
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

    person: Annotated[
        str,
        Field(None,
              description='Person that author is matched',
              min_length=1)]

    unique: AinswerMemoryUniqueField

    message: AinswerMemoryMessageField

    create: Annotated[
        str,
        Field(...,
              description='When the record was created',
              min_length=20,
              max_length=32)]


    def __init__(
        self,
        record: Optional[AinswerMemoryTable] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params: DictStrAny

        fields = [
            'plugin',
            'person',
            'unique',
            'message',
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



class AinswerMemory:
    """
    Store the historical information for the person memory.

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

        sengine = create_engine(
            self.__connect,
            pool_pre_ping=True)

        (SQLBase.metadata
         .create_all(sengine))

        session = (
            sessionmaker(sengine))

        self.__sengine = sengine
        self.__session = session


    def insert(
        self,
        *,
        person: str,
        message: str,
    ) -> None:
        """
        Insert the record into the historical person memorables.
        """

        plugin = self.__plugin

        sess = self.__session()
        lock = self.__locker

        table = AinswerMemoryTable
        model = AinswerMemoryRecord


        seed = (
            f'{Time().mpoch}'
            f'::{randint(0, 100)}'
            f'::{randint(0, 100)}'
            f'::{randint(0, 100)}')

        unique = Hashes(seed).uuid


        inputs: DictStrAny = {
            'plugin': plugin.name,
            'unique': unique,
            'person': person,
            'message': message,
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


        self.expunge(record.person)


    def expunge(
        self,
        person: str,
    ) -> None:
        """
        Remove the expired historical person memorable records.

        :param person: Unique identifier for the person object.
        """

        plugin = self.__plugin
        params = plugin.params

        maximum = params.memories


        sess = self.__session()
        lock = self.__locker

        table = AinswerMemoryTable

        _plugin = table.plugin
        _person = table.person
        _create = table.create


        with lock, sess as session:

            total = (
                session.query(table)
                .filter(
                    _plugin == plugin.name,
                    _person == person)
                .count())

            if total <= maximum:
                return

            cutoff = (
                session.query(_create)
                .filter(
                    _plugin == plugin.name,
                    _person == person)
                .order_by(_create.desc())
                .offset(maximum - 1)
                .limit(1).scalar())

            if cutoff is None:
                return NCNone

            (session.query(table)
             .filter(
                 _plugin == plugin.name,
                 _person == person,
                 _create < cutoff)
             .delete(
                synchronize_session=False))

            session.commit()


    def delete(
        self,
        person: str,
        unique: str,
    ) -> None:
        """
        Delete the record from the historical person memorables.

        :param person: Unique identifier for the person object.
        :param unique: Unique identifier for person memorable.
        """

        plugin = self.__plugin


        sess = self.__session()
        lock = self.__locker

        table = AinswerMemoryTable

        _plugin = table.plugin
        _person = table.person
        _unique = table.unique


        with lock, sess as session:

            (session.query(table)
             .filter(
                 _plugin == plugin.name,
                 _person == person,
                 _unique == unique)
             .delete(
                synchronize_session=False))

            session.commit()


    def records(
        self,
        mitem: 'RobieMessage',
    ) -> list[AinswerMemoryRecord]:
        """
        Return the historical records for the person memorables.

        :param mitem: Item containing information for operation.
        :returns: Historical records for the person memorables.
        """

        assert mitem.person

        return self.search(
            person=mitem.person)


    def search(
        self,
        *,
        person: Optional[str] = None,
        unique: Optional[str] = None,
    ) -> list[AinswerMemoryRecord]:
        """
        Return the historical records for the person memorables.

        :returns: Historical records for the person memorables.
        """

        plugin = self.__plugin


        sess = self.__session()
        lock = self.__locker

        records: list[AinswerMemoryRecord]

        table = AinswerMemoryTable
        model = AinswerMemoryRecord

        _plugin = table.plugin
        _person = table.person
        _unique = table.unique
        _create = table.create


        with lock, sess as session:

            records = []

            query = (
                session.query(table)
                .filter(
                    _plugin == plugin.name)
                .order_by(_create.desc()))

            if person is not None:
                query = query.filter(
                    _person == person)

            if unique is not NCNone:
                query = query.filter(
                    _unique == unique)


            for record in query.all():

                object = model(record)

                records.append(object)

            return records[::-1]
