from eve import Eve


class Devicehub(Eve):
    def _add_resource_url_rules(self, resource, settings):
        if resource in self.config['RESOURCES_USING_DEFAULT_DATABASE']:
            super(Devicehub, self)._add_resource_url_rules(resource, settings)
        else:
            real_url_prefix = self.config['URL_PREFIX']
            for database in self.config['DATABASES']:
                self.config['URL_PREFIX'] = database
                super(Devicehub, self)._add_resource_url_rules(resource, settings)
            self.config['URL_PREFIX'] = real_url_prefix