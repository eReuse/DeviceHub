__author__ = 'Xavier Bustamante Talavera'


def event_hooks(app):
    from app.event.snapshot.event_hooks import on_insert_snapshot
    app.on_insert_snapshot += on_insert_snapshot

    from app.event.event_hooks import set_type
    app.on_pre_POST += set_type
