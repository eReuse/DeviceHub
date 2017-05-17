Other endpoints
===============

Export to spreadsheets
----------------------
.. http:get:: (string:database)/export/(string:resource)

    Exports a set of devices to a spreadsheet file. This set can be defined by a list of ids.
    If resource is 'devices', this endpoints returns a spreadsheet with all the devices from the passed-in ids.
    If resource is any group, it returns a spreadsheet (page) for each id (a group label), containing all devices
    inside the group.

    Note that exporting is limited to PAGINATION_LIMIT (a thing to resolve when updating to next eve's version).

    :query ids: If resource is ``devices``, a list of device ids, otherwise a list of group labels.
    :query type: Optional. Either ``detailed`` or ``basic``. The former retreives more information than the latter.
                 By default it is ``detailed``.
    :reqheader Accept:
        An ordered list of mime types representing the type of returned file. It needs to be one accepted by
        pyexcel. Examples are: ``application/vnd.oasis.opendocument.spreadsheet`` for ods or
        ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`` for xlsx.
    :statuscode 200: The spreadsheets are returned in a file.
    :statuscode 406: The server can't generate the requested type of spreadsheet.
