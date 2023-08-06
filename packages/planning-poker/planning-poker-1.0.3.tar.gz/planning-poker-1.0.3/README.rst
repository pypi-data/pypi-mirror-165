Planning Poker
==============

.. image:: https://codecov.io/gh/rheinwerk-verlag/planning-poker/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/rheinwerk-verlag/planning-poker
   :alt: Code Coverage

.. image:: https://readthedocs.org/projects/planning-poker/badge/?version=stable
   :target: https://planning-poker.readthedocs.io/en/stable/?badge=stable
   :alt: Documentation Status

The idea for the Planning Poker app came to life during the 2020 Covid pandemic with the aim to provide agile teams with
an easy way to perform their planning poker sessions from the safety of their homes. It was developed with flexibility
and extensibility in mind. Powered by a Django backend and a frontend written in Vue.js.

Features
--------
* 🔍 This app comes with an **easy-to-use interface** and provides all the necessary data for estimating the scope of
  your stories on a single page.
* 🗳️ The users are separated into **voters** and **moderators** who see and do different things during a session.
  See `roles <https://planning-poker.readthedocs.io/en/stable/user_docs/roles.html>`_ for more information.
* 👥 See who participates in your session via a **live updated list of participants**.
* 🌙 Natively supported **dark mode**.


Screenshots
-----------
.. figure:: https://raw.githubusercontent.com/rheinwerk-verlag/planning-poker/main/docs/static/ui_overview.png
   :width: 100%
   :alt: You can see all the necessary information on a single page

   You can see all the necessary information on a single page

.. figure:: https://raw.githubusercontent.com/rheinwerk-verlag/planning-poker/main/docs/static/participants_overview.gif
   :width: 100%
   :alt: Live updated list of participants

   Live updated list of participants

.. figure:: https://raw.githubusercontent.com/rheinwerk-verlag/planning-poker/main/docs/static/dark_mode.png
   :width: 100%
   :alt: Natively supported dark mode

   Natively supported dark mode

Quickstart
----------
Basic understanding of Python and Django is not required but definitely recommended before you start installing this
application.

Do you have Django installed? Follow these steps `here <https://docs.djangoproject.com/en/stable/topics/install/>`_ if
you haven't.

Following these steps will give you a site which you can use to test the Planning Poker App.

#. Have an existing project where you want to include the Planning Poker app or create a new one. ::

    $ django-admin startproject planning_poker_site

#. Install the app via pip. ::

    $ pip install planning-poker

#. Configure your settings. They are located in ``planning_poker_site/settings.py`` if you chose to setup a new
   project. You'll find the minimal settings required for the Planning Poker app below. See
   `configuration <https://planning-poker.readthedocs.io/en/stable/user_docs/configuration.html>`_ for more ways to
   customize the application to fit your needs.

   .. code-block:: python

        ...

        INSTALLED_APPS = [
            ...
            'django.contrib.humanize',
            'channels',
            'planning_poker.apps.ChannelsPresenceConfig',
            'planning_poker'
        ]

        ASGI_APPLICATION = 'planning_poker_site.routing.application'

        # This is not the optimal channel layer and should not be used for production.
        # See https://channels.readthedocs.io/en/stable/topics/channel_layers.html for an alternative.
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels.layers.InMemoryChannelLayer'
            }
        }

        LOGIN_URL = 'admin:login'
        LOGOUT_URL = 'admin:logout'

#. Create a ``routing.py`` with the following content.

   .. code-block:: python

    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    import planning_poker.routing

    application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(URLRouter(planning_poker.routing.websocket_urlpatterns)),
    })

#. Include ``planning_poker``'s URLs in your urls which can be found in ``planning-poker-site/urls.py`` in the
   fresh project.

   .. code-block:: python

    from django.contrib import admin
    from django.urls import include, path
    from django.views.generic.base import RedirectView

    urlpatterns = [
        path('admin/', admin.site.urls),
        # The first entry isn't needed but nice to have if the sole purpose of this project is serving the Planning Poker app.
        path('', RedirectView.as_view(pattern_name='planning_poker:index'), name='redirect_to_poker_index'),
        path('poker/', include('planning_poker.urls')),
    ]

#. Run the migrations. ::

    $ python manage.py migrate

#. You can now start your server. ::

    $ python manage.py runserver 0.0.0.0:8000

See the `user documentation <https://planning-poker.readthedocs.io/en/stable/user_docs/index.html>`_ for more
information on how to use the Planning Poker app.
