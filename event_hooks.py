__author__ = 'Xavier Bustamante Talavera'

def event_hooks(app):
    from app.event.snapshot.event_hooks import on_insert_snapshot
    app.on_insert_snapshot += on_insert_snapshot

    from app.event.event_hooks import set_type
    app.on_pre_POST += set_type

    from app.event.add.event_hooks import add_components
    app.on_post_POST_add += add_components

    from app.event.register.event_hooks import set_components
    app.on_post_POST_register += set_components

    from app.event.remove.event_hooks import remove_components
    app.on_post_POST_remove += remove_components
