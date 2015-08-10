__author__ = 'busta'


def event_hooks(app):
    from app.event.event_hooks import pre_get_event
    from app.event.register.event_hooks import pre_get_register, pre_post_register
    app.on_pre_GET_events += pre_get_event
    app.on_pre_GET_registers += pre_get_register
    app.on_pre_POST_registers += pre_post_register
