from ereuse_devicehub.resources.schema import RDFS


class Condition(RDFS):
    """Grades the state of the device in different areas."""
    aesthetic = Aesthetic
    functional = Functional


class ConditionType(RDFS):
    """Abstract class to provide 'general' field."""
    general = {
        'type': 'scale5',
        'description': 'Grade the device for this category [0 bad condition - 5 perfect condition].'
    }


class Aesthetic(ConditionType):
    """Grades the visual condition of a device in different aspects."""
    scratches = {
        'type': 'scale5',
        'description': 'Has it scratches on the case? [0 none - 5 many and notorious]'
    }
    paint = {
        'type': 'scale5',
        'description': 'Has it imperfections on the painting? [0 none - 5 many and notorious]'
    }
    numberOfButtonsNotWorking = {
        'type': 'natural',
        'description': 'How many keys or buttons are not working?'
    }
    scratchesOnScreen = {
        'type': 'scale5',
        'description': 'Has it scratches on the screen? [0 none - 5 many and notorious]',
        'doc': 'Only computes on ComputerMonitor, Laptop, Netbook and Mobile'
    }


class Functional(ConditionType):
    """Grades how performs a device."""
    # todo add tests in here?
    visualDefectsInImage = {
        'type': 'scale5',
        'description': 'Has the image of the screen present visual imperfections? [0 none - 5 many and notorious]'
    }
