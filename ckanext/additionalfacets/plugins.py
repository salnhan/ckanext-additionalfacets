import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import json
import os
import pylons.config as config


from ckanext.additionalfacets import loader
from ckanext.additionalfacets import helpers as additional_facets_helpers

class AdditionalFacetsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)

    # Constants
    ADDITIONAL_FACETS_CONFIG = 'ckanext.additional_facets'
    DISPLAY_FACETS_ON_GROUPS_PAGE = 'ckanext.additional_facets.display_on_group_page'
    DISPLAY_FACETS_ON_ORG_PAGE = 'ckanext.additional_facets.display_on_org_page'


    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        facets_inputs = config.get(self.ADDITIONAL_FACETS_CONFIG, '').split()

        # get additional facets from the first input
        self.additional_facets = loader.get_additional_facets(facets_inputs[0])
        self.display_facets_on_group_page = toolkit.asbool(config.get(self.DISPLAY_FACETS_ON_GROUPS_PAGE, False))
        self.display_facets_on_org_page = toolkit.asbool(config.get(self.DISPLAY_FACETS_ON_ORG_PAGE, False))


    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        '''
        Insert additional facets to dataset search page
        '''
        language = additional_facets_helpers.lang()
        # additional_facets = self._get_facets_label(language)
        additional_facets = self._get_facets_with_translation()
        facets_dict.update(additional_facets)

        return facets_dict


    def group_facets(self, facets_dict, group_type, package_type):
        '''
        Insert additional facets to group search page
        '''
        if self.display_facets_on_group_page:
            language = additional_facets_helpers.lang()
            additional_facets = self._get_facets_label(language)
            facets_dict.update(additional_facets)

        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        '''
        Insert additional facets to organization search page
        '''
        if self.display_facets_on_group_page:
           language = additional_facets_helpers.lang()
           additional_facets = self._get_facets_label(language)
           facets_dict.update(additional_facets)

        return facets_dict


    # Private methods
    def _get_facets_with_translation(self):
        language = additional_facets_helpers.lang()
        facets = self.additional_facets['facets']
        additional_facets_name = {}
        if not facets:
            return additional_facets_name
        
        for facet in facets:
            additional_facets_name[facet['dataset_field']] = facet['facet_name'][language]

        return additional_facets_name