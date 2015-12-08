import asyncio
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from django.conf import settings
from django.utils import timezone


def send_message(key, message, *args, **kwargs):
    if settings.USE_WAMP:
        class Component(ApplicationSession):
            @asyncio.coroutine
            def onJoin(self, details):
                self.publish(u'lechbot.say', {
                    'key': key,
                    'time': timezone.utcnow(),
                    'text': message.format(*args, **kwargs),
                    'meta': [args, kwargs],
                })

        runner = ApplicationRunner(
            settings.CROSSBAR_URL,
            settings.CROSSBAR_REALM,
            debug_wamp=settings.DEBUG,
            debug=settings.DEBUG,
        )
        runner.run(Component)
