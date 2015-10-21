__author__ = 'Xavier Bustamante Talavera'

def event_hooks(app):
    from app.event.snapshot.event_hooks import on_insert_snapshot
    app.on_insert_snapshot += on_insert_snapshot

    from app.event.event_hooks import set_type, embed
    app.on_pre_POST += set_type
    app.on_fetched_resource += embed

    from app.event.add.event_hooks import add_components
    app.on_post_POST_add += add_components

    from app.event.register.event_hooks import set_components
    app.on_post_POST_register += set_components

    from app.event.remove.event_hooks import remove_components
    app.on_post_POST_remove += remove_components

    from app.device.event_hooks import embed_components
    app.on_fetched_resource += embed_components
    app.on_fetched_item += embed_components
   # app.on_fetched_item += embed_components

    from app.event.logger.settings import get_info_from_hook
    app.on_inserted += get_info_from_hook

    from app.accounts.event_hooks import add_token
    app.on_insert_accounts += add_token
