__author__ = 'Xavier Bustamante Talavera'

def event_hooks(app):
    """
    pre_POST methods are not executed by post_internal
    :param app:
    :return:
    """
    from app.event.snapshot.event_hooks import on_insert_snapshot
    app.on_insert_snapshot += on_insert_snapshot

    from app.event.event_hooks import embed, get_place
    app.on_fetched_resource += embed
    app.on_insert += get_place


    from app.event.add.event_hooks import add_components
    app.on_post_POST_add += add_components

    from app.event.register.event_hooks import set_components
    app.on_post_POST_register += set_components

    from app.event.remove.event_hooks import remove_components
    app.on_post_POST_remove += remove_components

    from app.device.event_hooks import embed_components
    app.on_fetched_resource += embed_components
    app.on_fetched_item += embed_components

    from app.event.logger.settings import get_info_from_hook
    app.on_inserted += get_info_from_hook

    from app.accounts.event_hooks import add_token, block_users
    app.on_insert_accounts += add_token
    app.on_insert_accounts += block_users  # Block users by default

    from app.Utils import set_byUser
    app.on_insert += set_byUser

    from app.place.event_hooks import set_place_in_devices, update_place_in_devices, unset_place_in_devices
    #app.on_inserted_places += add_children,
    app.on_inserted_places += set_place_in_devices
    app.on_updated_places += update_place_in_devices
    app.on_deleted_places += unset_place_in_devices

