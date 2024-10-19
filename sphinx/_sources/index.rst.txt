Enasis Network Chatting Robie
=============================

Configuration Container
-----------------------

.. autoclass:: enrobie.robie.RobieConfig
   :members:
   :show-inheritance:
   :noindex:

Parameters Container
--------------------

.. autopydantic_model:: enrobie.robie.params.RobieParams
   :members:
   :show-inheritance:
   :noindex:

Robie Clients
-------------

.. autopydantic_model:: enrobie.clients.discord.params.DSCClientParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enrobie.clients.irc.params.IRCClientParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enrobie.clients.mattermost.params.MTMClientParams
   :members:
   :show-inheritance:
   :noindex:

Robie Plugins
-------------

.. autopydantic_model:: enrobie.plugins.autojoin.params.AutoJoinPluginParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enrobie.plugins.autonick.params.AutoNickPluginParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enrobie.plugins.status.params.StatusPluginParams
   :members:
   :show-inheritance:
   :noindex:
