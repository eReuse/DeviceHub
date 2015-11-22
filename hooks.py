def event_hooks(app):
    """
    pre_POST methods are not executed by post_internal
    :param app:
    :return:
    """
    from app.utils import set_jsonld_link
    app.on_post_GET += set_jsonld_link

    from app.device.hooks import generate_etag
    app.on_insert += generate_etag

    from app.security.hooks import project_item, project_resource
    app.on_fetched_item += project_item
    app.on_fetched_resource += project_resource

    from app.event.snapshot.hooks import on_insert_snapshot, save_request
    app.on_insert_snapshot += on_insert_snapshot
    app.on_insert_snapshot += save_request

    from app.event.hooks import get_place
    app.on_insert += get_place

    from app.event.add.hooks import add_components
    app.on_inserted_add += add_components

    from app.event.register.hooks import post_devices
    app.on_insert_register += post_devices

    from app.event.remove.hooks import remove_components
    app.on_inserted_remove += remove_components

    #app.on_inserted += get_info_from_hook

    from app.account.hooks import add_token, block_users
    app.on_insert_accounts += add_token
    app.on_insert_accounts += block_users  # Block users by default

    from app.account.hooks import set_byUser
    app.on_insert += set_byUser

    from app.place.hooks import set_place_in_devices, update_place_in_devices, unset_place_in_devices
    app.on_inserted_places += set_place_in_devices
    app.on_updated_places += update_place_in_devices
    app.on_deleted_places += unset_place_in_devices
