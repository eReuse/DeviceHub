def event_hooks(app):
    """
    pre_POST methods are not executed by post_internal
    :param app:
    :return:
    """
    from ereuse_devicehub.utils import set_response_headers_and_cache, redirect_on_browser
    app.on_post_GET += set_response_headers_and_cache
    app.on_pre_GET += redirect_on_browser

    from ereuse_devicehub.security.hooks import project_item, project_resource, authorize_public, deny_public
    app.on_fetched_item += authorize_public
    app.on_fetched_resource += deny_public
    app.on_fetched_item += project_item
    app.on_fetched_resource += project_resource

    from ereuse_devicehub.resources.device.hooks import generate_etag, get_icon, get_icon_resource, autoincrement, post_benchmark, \
        materialize_public_in_components, materialize_public_in_components_update
    app.on_insert += generate_etag
    app.on_fetched_item += get_icon
    app.on_fetched_resource += get_icon_resource
    app.on_insert += autoincrement
    app.on_insert += post_benchmark
    app.on_inserted += materialize_public_in_components
    app.on_updated += materialize_public_in_components_update

    from ereuse_devicehub.resources.event.snapshot.hooks import on_insert_snapshot, save_request, materialize_test_hard_drives, \
        materialize_erase_basic, set_secured
    app.on_insert_snapshot += set_secured
    app.on_insert_snapshot += on_insert_snapshot
    app.on_insert_snapshot += save_request
    app.on_inserted_snapshot += materialize_test_hard_drives
    app.on_inserted_snapshot += materialize_erase_basic

    from ereuse_devicehub.resources.event.hooks import get_place, materialize_components, materialize_parent, set_place
    app.on_insert += get_place
    app.on_insert += set_place
    app.on_insert += materialize_components
    app.on_insert += materialize_parent


    from ereuse_devicehub.resources.event.add.hooks import add_components
    app.on_inserted_add += add_components

    from ereuse_devicehub.resources.event.register.hooks import post_devices
    app.on_insert_register += post_devices

    from ereuse_devicehub.resources.event.remove.hooks import remove_components
    app.on_inserted_remove += remove_components

    from ereuse_devicehub.resources.event.allocate.hooks import materialize_actual_owners_add, avoid_repeating_allocations, set_organization
    app.on_insert_allocate += avoid_repeating_allocations
    app.on_inserted_allocate += materialize_actual_owners_add
    app.on_insert_allocate += set_organization

    from ereuse_devicehub.resources.event.deallocate.hooks import materialize_actual_owners_remove, set_organization
    app.on_inserted_deallocate += materialize_actual_owners_remove
    app.on_insert_deallocate += set_organization

    if app.config.get('LOGGER', True):
        from ereuse_devicehub.resources.event.logger.hooks import get_info_from_hook
        app.on_inserted += get_info_from_hook

    from ereuse_devicehub.resources.account.hooks import add_token, hash_password, set_default_database_if_empty
    app.on_insert_accounts += add_token
    app.on_insert_accounts += hash_password
    app.on_insert_accounts += set_default_database_if_empty

    from ereuse_devicehub.resources.account.hooks import set_byUser, add_or_get_inactive_account, set_byOrganization
    app.on_insert += set_byUser
    app.on_insert_receive += add_or_get_inactive_account  # We need to execute after insert and insert_resource as it
    app.on_insert_register += add_or_get_inactive_account  # deletes the 'unregistered...'
    app.on_insert_allocate += add_or_get_inactive_account
    app.on_insert += set_byOrganization

    from ereuse_devicehub.resources.event.receive.hooks import transfer_property, set_organization
    app.on_insert_receive += transfer_property
    app.on_insert_receive += set_organization

    from ereuse_devicehub.resources.place.hooks import set_place_in_devices, update_place_in_devices, unset_place_in_devices, update_place_in_devices_if_places, avoid_deleting_if_has_event
    app.on_inserted_places += set_place_in_devices
    app.on_updated_places += update_place_in_devices_if_places
    app.on_delete_item_places += avoid_deleting_if_has_event
    app.on_deleted_item_places += unset_place_in_devices
    app.on_replaced_places += update_place_in_devices
