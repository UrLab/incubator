import asyncio


from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that subscribes and receives events, and
    stop after having received 5 events.
    """

    @asyncio.coroutine
    def onJoin(self, details):

        self.received = 0

        def on_event(*args, **kwargs):
            print(args, kwargs)

        yield from self.subscribe(on_event, u'incubator.actstream')

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://snips.lan:8081/ws"),
        u"urlab",
        debug_wamp=False,  # optional; log many WAMP details
        debug=False,  # optional; log even more details
    )
    runner.run(Component)
