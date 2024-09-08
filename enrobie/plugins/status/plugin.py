"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING

from .params import StatusPluginParams
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...robie.threads import RobieThread



class StatusPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin responds to inquiries about Robie status.

    :param robie: Primary class instance for Chatting Robie.
    """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """


    def operate(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        robie = thread.robie
        mqueue = thread.mqueue
        member = thread.member
        cqueue = member.cqueue
        params = self.params

        assert isinstance(
            params, StatusPluginParams)

        command = params.command
        match: Optional[str]


        while not mqueue.empty:

            mitem = mqueue.get()

            family = mitem.family

            event = getattr(
                mitem, 'event')


            match = None

            if family == 'irc':
                match = command.irc

            if family == 'discord':
                match = command.dsc

            if family == 'mattermost':
                match = command.mtm

            if match is None:
                continue  # NOCVR


            message = event.message

            if message != match:
                continue


            citem = mitem.reply(
                robie,
                'All good here')

            cqueue.put(citem)
