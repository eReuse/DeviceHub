from collections import OrderedDict

from graphviz import Digraph
from app.utils import Naming

class ToClassDiagram:
    """
        Converts the API Schema to an UML Class Diagram.

        To use this module, install 'graphviz' through pip and just execute the class: Graphviz()
        You can add 2 parameters, the location of the file and the type.
    """

    def __init__(self, app):
        self.dot = Digraph()
        for name, resource in app.config['DOMAIN'].items():
            if 'is_super_class_of' in resource:
                self.generate_class(Naming.resource(name), resource, {})
        self.dot.render('diagram.sv', None, True)

    def generate_class(self, resource_name, settings, parent_schema):
        schema = OrderedDict()
        for key in set(settings['original_schema'].keys()) - set(parent_schema.keys()):
            schema[key] = settings['original_schema'][key]

        self.dot.node(resource_name, '{}|{}'.format(resource_name, '\l'.join(self.print_schema_fields(resource_name, schema))))
        if 'is_super_class_of' in settings:
            for sub_name, sub_settings in settings['is_super_class_of']['references'].items():
                self.generate_class(Naming.resource(sub_name), sub_settings, schema)
                self.dot.edge(Naming.resource(sub_name), resource_name, arrowhead='empty')

    def print_schema_fields(self, resource_name, schema: OrderedDict):
        fields = []
        for field_name, settings in schema.items():

            if 'data_relation' in settings:
                if settings['type'] != 'list':
                    head_label = '1' if settings.get('required', False) else '0..1'
                else:
                    head_label = '*' if settings.get('required', False) else '1..*'
                self.dot.edge(resource_name, settings['data_relation']['resource'], headlabel=head_label, taillabel='*', label=field_name)
            else:
                field = '+ {}'.format(field_name)
                if len(settings.get('allowed', set())) > 0:
                    self.dot.node('{}Enum'.format(resource_name), '{}Enum\lEnum'.format(resource_name, '\l'.join(map(str,settings['allowed']))))
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

