# -*- coding:utf-8 -*-


class EventDispatcher(Publisher):
    """ provides an event dispatcher method via dependency injection.

    Events emitted will be dispatched via the service's events exchange,
    which automatically gets declared by the event dispatcher
    as a topic exchange.
    The name for the exchange will be `{service-name}.events`.

    Events, emitted via the dispatcher, will be serialized and published
    to the events exchange. The event's type attribute is used as the
    routing key, which can be used for filtering on the listener's side.

    The dispatcher will return as soon as the event message has been published.
    There is no guarantee that any service will receive the event, only
    that the event has been successfully dispatched.

    Example::

        class Spammer(object):
            dispatch_spam = EventDispatcher()

            def emit_spam(self):
                evt_data = 'ham and eggs'
                self.dispatch_spam('spam.ham', evt_data)

    """

    def setup(self):
        self.exchange = get_event_exchange(self.container.service_name)
        self.declare.append(self.exchange)
        super(EventDispatcher, self).setup()

    def get_dependency(self, worker_ctx):
        """ Inject a dispatch method onto the service instance
        """
        extra_headers = self.get_message_headers(worker_ctx)

        def dispatch(event_type, event_data):
            self.publisher.publish(
                event_data,
                exchange=self.exchange,
                routing_key=event_type,
                extra_headers=extra_headers
            )

        return dispatch