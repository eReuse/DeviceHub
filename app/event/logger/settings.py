from app.event.Event import Event

__author__ = 'busta'


def register_logging_events(app):
    for event in Event.get_types():
        setattr(app, "on_post_POST_" + event.lower(), get_info_from_hook)


def get_info_from_hook( resource:str, request, response):
    """
    Send info from the hook to the Logger in its thread
    :param resource:
    :param request:
    :param response:
    :return:
    """
    pass
