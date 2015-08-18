__author__ = 'Xavier Bustamante Talavera'


def event_hooks(app):
    from app.event.snapshot.event_hooks import pre_post_snapshot
    app.on_pre_POST_snapshot += pre_post_snapshot

