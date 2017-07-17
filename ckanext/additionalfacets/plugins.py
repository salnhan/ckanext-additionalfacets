import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

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
        '''
        Get the translated facet title
        '''
        # name of additional facets
        additional_facets_name = {}

        # get all additional facets
        facets = self.additional_facets['facets']

        # stop if the facet list is empty
        if not facets:
            return additional_facets_name

        # get current environment's language
        language = additional_facets_helpers.lang()

        # search and get the translated title for facet
        for facet in facets:
            additional_facets_name[facet['dataset_field']] = facet['facet_name'][language]

        return additional_facets_name


    def _get_translated_label_of_facet_item(self, dataset_facet_field, default_facet_label):
        '''
        Translate the default label of facet item. Return the default facet label if no translation available
        :param dataset_facet_field: the name of facet field in the dataset
        :param default_facet_label: the default label of the facet item
        '''

        # get all additional facets
        facets = self.additional_facets['facets']
         # if facets not empty
        if facets:
            for facet in facets:
                # get the concrete facet
                if facet['dataset_field'] == dataset_facet_field:
                    facet_items = facet['facet_items']
                    for facet_item in facet_items:
                        # translate the label of facet
                        if facet_item['default_label'] == default_facet_label:
                            language = additional_facets_helpers.lang()
                            default_facet_label = facet_item['new_label'][language]

        return default_facet_label



    ## Define own helpers
    def get_helpers(self):
        return {
            # This helper function will be called in snippets/facet_list.html
           'additionalfacets_translate_facet_item_label': self._get_translated_label_of_facet_item
        }