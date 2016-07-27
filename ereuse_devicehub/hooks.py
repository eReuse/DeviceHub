
def hooks(app):
    """
        This method "ties" all the hooks DeviceHub uses with the app.
    """
    from ereuse_devicehub.resources.hooks import set_response_headers_and_cache, redirect_on_browser, set_sameAs
    app.on_post_GET += set_response_headers_and_cache
    app.on_pre_GET += redirect_on_browser
    app.on_insert += set_sameAs

    from ereuse_devicehub.security.hooks import project_item, project_resource, authorize_public, deny_public
    app.on_fetched_item += authorize_public
    app.on_fetched_resource += deny_public
    app.on_fetched_item += project_item
    app.on_fetched_resource += project_resource

    from ereuse_devicehub.resources.device.hooks import generate_etag, get_icon, get_icon_resource, autoincrement, \
        post_benchmark, \
        materialize_public_in_components, materialize_public_in_components_update
    app.on_insert += generate_etag
    app.on_fetched_item += get_icon
    app.on_fetched_resource += get_icon_resource
    app.on_insert += autoincrement
    app.on_insert += post_benchmark
    app.on_inserted += materialize_public_in_components
    app.on_updated += materialize_public_in_components_update

    from ereuse_devicehub.resources.event.device.snapshot.hooks import on_insert_snapshot, save_request, \
        materialize_test_hard_drives, \
        materialize_erase_basic, set_secured
    app.on_insert_devices_snapshot += set_secured
    app.on_insert_devices_snapshot += on_insert_snapshot
    app.on_insert_devices_snapshot += save_request
    app.on_inserted_devices_snapshot += materialize_test_hard_drives
    app.on_inserted_devices_snapshot += materialize_erase_basic

    from ereuse_devicehub.resources.event.device.hooks import get_place, materialize_components, materialize_parent, \
        set_place
    app.on_insert += get_place
    app.on_insert += set_place
    app.on_insert += materialize_components
    app.on_insert += materialize_parent

    from ereuse_devicehub.resources.event.device.add.hooks import add_components
    app.on_inserted_devices_add += add_components

    from ereuse_devicehub.resources.event.device.register.hooks import post_devices
    app.on_insert_devices_register += post_devices

    from ereuse_devicehub.resources.event.device.remove.hooks import remove_components
    app.on_inserted_devices_remove += remove_components

    from ereuse_devicehub.resources.event.device.allocate.hooks import avoid_repeating_allocations, \
        materialize_actual_owners_add, set_organization
    app.on_insert_devices_allocate += avoid_repeating_allocations
    app.on_inserted_devices_allocate += materialize_actual_owners_add
    app.on_insert_devices_allocate += set_organization

    from ereuse_devicehub.resources.event.device.deallocate.hooks import materialize_actual_owners_remove, \
        set_organization
    app.on_inserted_devices_deallocate += materialize_actual_owners_remove
    app.on_insert_devices_deallocate += set_organization

    if app.config.get('SUBMITTER', True):
        from ereuse_devicehub.resources.submitter.grd_submitter.hooks import submit_events_to_grd
        app.on_inserted += submit_events_to_grd

    from ereuse_devicehub.resources.account.hooks import add_token, hash_password, set_default_database_if_empty
    app.on_insert_accounts += add_token
    app.on_insert_accounts += hash_password
    app.on_insert_accounts += set_default_database_if_empty

    from ereuse_devicehub.resources.account.hooks import set_byUser, add_or_get_inactive_account, set_byOrganization
    app.on_insert += set_byUser
    app.on_insert_devices_receive += add_or_get_inactive_account  # We need to execute after insert and insert_resource as it
    app.on_insert_devices_register += add_or_get_inactive_account  # deletes the 'unregistered...'
    app.on_insert_devices_allocate += add_or_get_inactive_account
    app.on_insert += set_byOrganization

    from ereuse_devicehub.resources.event.device.receive.hooks import transfer_property, set_organization
    app.on_insert_devices_receive += transfer_property
    app.on_insert_devices_receive += set_organization

    from ereuse_devicehub.resources.place.hooks import set_place_in_devices, update_place_in_devices, \
        unset_place_in_devices, update_place_in_devices_if_places, avoid_deleting_if_has_event
    app.on_inserted_places += set_place_in_devices
    app.on_updated_places += update_place_in_devices_if_places
    app.on_delete_item_places += avoid_deleting_if_has_event
    app.on_deleted_item_places += unset_place_in_devices
    app.on_replaced_places += update_place_in_devices

    # Device materializations
    from ereuse_devicehub.resources.device.hooks import MaterializeEvents
    app.on_inserted += MaterializeEvents.materialize_events
