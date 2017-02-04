def resources(app):
    """
    Obtains all resourceSettings and their schemas
    :param app:
    :return:
    """
    # Adding the leaves is more than enough (although otherwise does not harm)
    from ereuse_devicehub.resources.device.settings import DeviceSettings
    app.resource_proxy.add(DeviceSettings)

    from ereuse_devicehub.resources.account.settings import AccountSettings
    app.resource_proxy.add(AccountSettings)
