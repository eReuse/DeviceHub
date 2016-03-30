from collections import OrderedDict

from graphviz import Digraph

from app.device.schema import Device
from app.event.settings import Event
from app.schema import RDFS
from app.utils import Naming

class ToClassDiagram:
    """
        Converts the API Schema to an UML Class Diagram.

        To use this module, install 'graphviz' through pip and just execute the class: Graphviz()
        You can add 2 parameters, the location of the file and the type.
    """

    def __init__(self, app):
        self.g = Digraph(format='png')
        self.g.attr('node', shape='record')
        self.classes = Digraph()
        self.enums = Digraph()
        self.devices = Digraph()
        self.events = Digraph()
        self.generate_class(RDFS, self.classes)
        device_subclasses = Device.get_all_subclasses() + [Device]
        event_subclasses = Event.get_all_subclasses() + [Event]
        for subclass in RDFS.get_all_subclasses():
            if subclass in device_subclasses:
                self.generate_class(subclass, self.devices)
            elif subclass in event_subclasses:
                self.generate_class(subclass, self.events)
            else:
                self.generate_class(subclass, self.classes)
        self.g.subgraph(self.classes)
        self.g.subgraph(self.enums)
        self.g.subgraph(self.events)
        self.g.subgraph(self.devices)
        self.g.render('diagram.sv', None, True)

    def generate_class(self, cls, group):
        schema = OrderedDict(cls.actual_attributes())
        if cls != RDFS:
            del schema['@type']
        name = cls.type_name()
        group.node(name, '{{{}|{}}}'.format(name, '\l'.join(self.print_schema_fields(name, schema, group))))
        try:
            super_class = cls.get_super_classes(1)[1]
            group.edge(name, super_class.type_name(), arrowhead='empty')
        except AttributeError:
            pass

    def print_schema_fields(self, name: str, schema: OrderedDict, group):
        fields = []
        for field_name, settings in schema.items():
            if 'data_relation' in settings:
                if settings['type'] != 'list':
                    head_label = '1' if settings.get('required', False) else '0..1'
                else:
                    head_label = '*' if settings.get('required', False) else '1..*'
                group.edge(name, Naming.type(settings['data_relation']['resource']), headlabel=head_label, taillabel='*', label=field_name)
            else:
                field = '+ {}'.format(field_name)
                if len(settings.get('allowed', set())) > 0:
                    enum_name = '{}Enum'.format(name)
                    self.enums.node(enum_name, '{{{}Enum\lEnum|{}}}'.format(name, '\l'.join(map(str, settings['allowed']))))
                    field += ': {}'.format(enum_name)
                else:
                    field += ': {}'.format(settings['type'])
                if not settings.get('required', False):
                    field += ' [0..1]'
                if settings.get('writeonly', False):
                    field += ' (write-only)'
                if settings.get('readonly', False):
                    field += ' (read-only)'
                fields.append(field)
        return fields

