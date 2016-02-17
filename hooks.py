def event_hooks(app):
    """
    pre_POST methods are not executed by post_internal
    :param app:
    :return:
    """
    from app.utils import set_jsonld_link
    app.on_post_GET += set_jsonld_link

    from app.device.hooks import generate_etag, get_icon, get_icon_resource, autoincrement
    app.on_insert += generate_etag
    app.on_fetched_item += get_icon
    app.on_fetched_resource += get_icon_resource
    app.on_insert += autoincrement

    from app.security.hooks import project_item, project_resource
    app.on_fetched_item += project_item
    app.on_fetched_resource += project_resource

    from app.event.snapshot.hooks import on_insert_snapshot, save_request, materialize_test_hard_drives, materialize_erase_basic
    app.on_insert_snapshot += on_insert_snapshot
    app.on_insert_snapshot += save_request
    app.on_inserted_snapshot += materialize_test_hard_drives
    app.on_inserted_snapshot += materialize_erase_basic

    from app.event.hooks import get_place, materialize_components, materialize_parent, set_place
    app.on_insert += get_place
    app.on_insert += set_place
    app.on_insert += materialize_components
    app.on_insert += materialize_parent


    from app.event.add.hooks import add_components
    app.on_inserted_add += add_components

    from app.event.register.hooks import post_devices
    app.on_insert_register += post_devices

    from app.event.remove.hooks import remove_components
    app.on_inserted_remove += remove_components

    from app.event.receive.hooks import transfer_property
    app.on_insert_receive += transfer_property

    from app.event.allocate.hooks import materialize_actual_owners_add, avoid_repeating_allocations
    app.on_insert_allocate += avoid_repeating_allocations
    app.on_inserted_allocate += materialize_actual_owners_add

    from app.event.deallocate.hooks import materialize_actual_owners_remove
    app.on_inserted_deallocate += materialize_actual_owners_remove

    if app.config.get('LOGGER', True):
        from app.event.logger.hooks import get_info_from_hook
        app.on_inserted += get_info_from_hook

    from app.account.hooks import add_token, hash_password, set_default_database_if_empty
    app.on_insert_accounts += add_token
    app.on_insert_accounts += hash_password
    app.on_insert_accounts += set_default_database_if_empty

    from app.account.hooks import set_byUser, add_or_get_inactive_account
    app.on_insert += set_byUser
    app.on_insert_receive += add_or_get_inactive_account  # We need to execute after insert and insert_resource as it
    app.on_insert_register += add_or_get_inactive_account  # deletes the 'unregistered...'
    app.on_insert_allocate += add_or_get_inactive_account

    from app.place.hooks import set_place_in_devices, update_place_in_devices, unset_place_in_devices
    app.on_inserted_places += set_place_in_devices
    app.on_updated_places += update_place_in_devices
    app.on_deleted_places += unset_place_in_devices
