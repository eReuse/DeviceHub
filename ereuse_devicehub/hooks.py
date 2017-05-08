def hooks(app):
    """
        This method "ties" all the hooks DeviceHub uses with the app.
    """
    from ereuse_devicehub.resources.hooks import set_response_headers_and_cache, redirect_on_browser, check_type
    app.on_post_GET += set_response_headers_and_cache
    app.on_pre_GET += redirect_on_browser
    app.on_insert += check_type

    from ereuse_devicehub.security.hooks import project_item, project_resource, authorize_public, deny_public
    app.on_fetched_item += authorize_public
    app.on_fetched_resource += deny_public
    app.on_fetched_item += project_item
    app.on_fetched_resource += project_resource

    from ereuse_devicehub.resources.hooks import avoid_deleting_if_not_last_event_or_more_x_minutes
    app.on_pre_DELETE += avoid_deleting_if_not_last_event_or_more_x_minutes

    from ereuse_devicehub.resources.device.hooks import avoid_deleting_if_device_has_migrate
    app.on_delete_item += avoid_deleting_if_device_has_migrate

    from ereuse_devicehub.resources.event.device.hooks import fill_devices_field_from_groups
    app.on_insert += fill_devices_field_from_groups  # This needs to go before any insert device event hook

    from ereuse_devicehub.resources.event.device.migrate.hooks import check_migrate, create_migrate, submit_migrate, \
        check_migrate_insert, check_migrate_update, remove_devices_from_place, return_same_as
    app.on_insert += check_migrate_insert
    app.on_delete_item += check_migrate
    app.on_update += check_migrate_update
    app.on_replace += check_migrate_update
    app.on_inserted_devices_migrate += submit_migrate
    app.on_insert_devices_migrate += create_migrate
    app.on_inserted_devices_migrate += remove_devices_from_place
    app.on_post_POST_devices_migrate += return_same_as

    from ereuse_devicehub.resources.device.hooks import generate_etag, autoincrement, post_benchmark, \
        materialize_public_in_components, materialize_public_in_components_update
    app.on_insert += generate_etag
    app.on_insert += autoincrement
    app.on_insert += post_benchmark
    app.on_inserted += materialize_public_in_components
    app.on_updated += materialize_public_in_components_update

    from ereuse_devicehub.resources.event.device.snapshot.hooks import on_insert_snapshot, save_request, \
        materialize_test_hard_drives, materialize_erase_basic, set_secured, delete_events, move_id
    from ereuse_devicehub.resources.event.device.hooks import validate_only_components_can_have_parents
    app.on_insert_devices_snapshot += validate_only_components_can_have_parents
    app.on_insert_devices_snapshot += set_secured
    app.on_insert_devices_snapshot += on_insert_snapshot
    app.on_insert_devices_snapshot += save_request
    app.on_inserted_devices_snapshot += materialize_test_hard_drives
    app.on_inserted_devices_snapshot += materialize_erase_basic
    app.on_delete_item += delete_events
    app.on_pre_POST_devices_snapshot = move_id

    from ereuse_devicehub.resources.event.device.hooks import get_place, materialize_components, materialize_parent, \
        set_place, unset_place, delete_events_in_device, remove_from_other_events
    app.on_insert += get_place
    app.on_inserted += set_place
    app.on_delete_item += unset_place
    app.on_insert += materialize_components
    app.on_insert += materialize_parent
    app.on_delete_item += delete_events_in_device
    app.on_delete_item += remove_from_other_events

    from ereuse_devicehub.resources.event.device.add.hooks import add_components, delete_components
    app.on_inserted_devices_add += add_components
    app.on_delete_item += delete_components

    from ereuse_devicehub.resources.event.device.register.hooks import post_devices, delete_device
    app.on_insert_devices_register += validate_only_components_can_have_parents
    app.on_insert_devices_register += post_devices
    app.on_delete_item += delete_device

    from ereuse_devicehub.resources.event.device.remove.hooks import check_remove, remove_components
    app.on_insert_devices_remove += check_remove
    app.on_inserted_devices_remove += remove_components

    from ereuse_devicehub.resources.account.hooks import set_byUser, set_byOrganization, \
        add_or_get_inactive_account_allocate, add_or_get_inactive_account_receive, add_or_get_inactive_account_snapshot
    app.on_insert += set_byUser
    app.on_insert_devices_receive += add_or_get_inactive_account_receive
    app.on_insert_devices_allocate += add_or_get_inactive_account_allocate
    app.on_insert_devices_snapshot += add_or_get_inactive_account_snapshot
    app.on_insert += set_byOrganization

    from ereuse_devicehub.resources.event.device.allocate.hooks import avoid_repeating_allocations, \
        materialize_actual_owners_add, set_organization, re_materialize_owners
    app.on_insert_devices_allocate += avoid_repeating_allocations
    app.on_inserted_devices_allocate += materialize_actual_owners_add
    app.on_insert_devices_allocate += set_organization
    app.on_deleted_item += re_materialize_owners

    from ereuse_devicehub.resources.event.device.deallocate.hooks import materialize_actual_owners_remove, \
        set_organization
    app.on_inserted_devices_deallocate += materialize_actual_owners_remove
    app.on_insert_devices_deallocate += set_organization

    from ereuse_devicehub.resources.submitter.grd_submitter.hooks import submit_events_to_grd
    app.on_inserted += submit_events_to_grd

    from ereuse_devicehub.resources.account.hooks import add_token, hash_password, set_default_database_if_empty
    app.on_insert_accounts += add_token
    app.on_insert_accounts += hash_password
    app.on_insert_accounts += set_default_database_if_empty

    from ereuse_devicehub.resources.event.device.receive.hooks import transfer_property, set_organization
    app.on_insert_devices_receive += transfer_property
    app.on_insert_devices_receive += set_organization

    from ereuse_devicehub.resources.group.hooks import set_children, delete_children, \
        update_children
    app.on_insert += set_children
    app.on_update += update_children
    app.on_delete_item += delete_children
    app.on_replace += update_children

    from ereuse_devicehub.resources.group.physical.place.hooks import avoid_deleting_if_has_event
    app.on_delete_item_places += avoid_deleting_if_has_event

    from ereuse_devicehub.resources.event.device.live.hooks import save_ip
    app.on_insert_devices_live += save_ip

    # Device materializations
    from ereuse_devicehub.resources.device.hooks import redirect_to_first_snapshot
    from ereuse_devicehub.resources.hooks import MaterializeEvents
    app.on_inserted += MaterializeEvents.materialize_events
    app.on_delete_item += MaterializeEvents.dematerialize_event
    app.on_pre_DELETE += redirect_to_first_snapshot

    from ereuse_devicehub.resources.hooks import set_date
    app.on_insert += set_date

    # group-log
    from ereuse_devicehub.resources.group.group_log.hooks import add_group_change_to_log, set_children, delete_children
    app.on_inserted += set_children
    app.on_deleted_item += delete_children
    app.on_updated += add_group_change_to_log
    app.on_replaced += add_group_change_to_log
