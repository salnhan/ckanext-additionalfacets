import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import os
import pylons.config as config


from ckanext.additionalfacets import loader
from ckanext.additionalfacets import helpers as additional_facets_helpers

########################################################
# Insert additional facets to the facets list in CKAN  #
########################################################
class AdditionalFacetsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)

    # Constants
    ADDITIONAL_FACETS_CONFIG = 'ckanext.additional_facets'
    DISPLAY_FACETS_ON_GROUPS_PAGE = 'ckanext.additional_facets.display_on_group_page'
    DISPLAY_FACETS_ON_ORG_PAGE = 'ckanext.additional_facets.display_on_org_page'
    CLEAR_DEFAULT_FACETS = 'ckanext.additional_facets.clear_default_facets'


    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        facets_inputs = config.get(self.ADDITIONAL_FACETS_CONFIG, '').split()

        # get additional facets from the first input
        self.additional_facets = loader.get_additional_facets(facets_inputs[0])
        self.display_facets_on_group_page = toolkit.asbool(config.get(self.DISPLAY_FACETS_ON_GROUPS_PAGE, False))
        self.display_facets_on_org_page = toolkit.asbool(config.get(self.DISPLAY_FACETS_ON_ORG_PAGE, False))
        self.clear_default_facets = toolkit.asbool(config.get(self.CLEAR_DEFAULT_FACETS, False))


    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        '''
        Insert additional facets to dataset search page
        '''
        # clear default facets
        if self.clear_default_facets:
            facets_dict.clear()

        additional_facets = self._get_facets_with_translation()
        facets_dict.update(additional_facets)

        return facets_dict


    def group_facets(self, facets_dict, group_type, package_type):
        '''
        Insert additional facets to group search page
        '''
        if self.display_facets_on_group_page:
            additional_facets = self._get_facets_with_translation()
            facets_dict.update(additional_facets)

        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        '''
        Insert additional facets to organization search page
        '''
        if self.display_facets_on_group_page:
           additional_facets = self._get_facets_with_translation()
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
            if facet['dataset_field'] and facet['facet_name']:
                if facet['facet_name'][language]:
                    additional_facets_name[facet['dataset_field']] = facet['facet_name'][language]
                else:
                    additional_facets_name[facet['dataset_field']] = facet['facet_name']

        return additional_facets_name


    def _translate_facet_item_label(self, dataset_facet_field, default_facet_label):
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
                if 'dataset_field' in facet and facet['dataset_field'] == dataset_facet_field and 'facet_items' in facet:
                    facet_items = facet['facet_items']
                    for facet_item in facet_items:
                        # translate the label of facet
                        if facet_item['default_label'] == default_facet_label:
                            language = additional_facets_helpers.lang()
                            if facet_item['new_label'][language]:
                                default_facet_label = facet_item['new_label'][language]

        return default_facet_label


    def _get_facet_item_label_with_translation(self, dataset_facet_field, default_facet_label):
        '''
        Get the translated label of facet item. Return the default facet label if no translation available
        :param dataset_facet_field: the name of facet field in the dataset
        :param default_facet_label: the default label of the facet item
        '''

        return _translate_facet_item_label(dataset_facet_field, default_facet_label)


    ## Define own helpers
    def get_helpers(self):
        return {
            # This helper function will be called in snippets/facet_list.html
           'additionalfacets_translate_facet_item_label': self._get_facet_item_label_with_translation
        }


########################################################
# Additional facets from schemas of extension scheming #
########################################################
class AdditionalFacetsFromSchemingDatasetPlugin(AdditionalFacetsPlugin):

    # Private methods
    def _get_dataset_type_of_facet(self, dataset_facet_field):
        '''
        Get the dataset type, which contains the facet
        :param dataset_facet_field: name of facet field in the dataset (e.g: `extras_information_category`)
        '''
        # get all additional facets
        facets = self.additional_facets['facets']
        # set default dataset
        dataset_type = 'dataset'
        # if facets not empty
        if facets:
            for facet in facets:
                # get the concrete facet
                if ('dataset_field' in facet) and (facet['dataset_field'] == dataset_facet_field) and ('dataset_type' in facet):
                    dataset_type = facet['dataset_type']

        return dataset_type


    def _get_value_from_scheming_choices_field(self, field, default_facet_label, language):
        '''
        :param dataset_facet_field: name of facet field in the dataset (e.g: `extras_information_category`)
        '''
        for entry in field:
            if entry['value'] == default_facet_label:
                if len(entry['label']) > 1 and type(entry['label']) is dict:
                    label_array = entry['label']
                    for key, value in label_array.iteritems():
                        if key == language:
                            if value is not None:
                                return value
                            else:
                                return default_facet_label
                    if value is not None:
                        return value
                    else:
                        return default_facet_label


    def _get_facet_item_label_with_translation(self, dataset_facet_field, default_facet_label):
        '''
        Translate the default label of facet item. Return the default facet label if no translation available
        :param dataset_facet_field: the name of facet field in the dataset
        :param default_facet_label: the default label of the facet item
        '''
        from ckanext.scheming import helpers as scheming_helpers
        package_type = self._get_dataset_type_of_facet(dataset_facet_field)
        schema = scheming_helpers.scheming_get_dataset_schema(package_type)
        language = scheming_helpers.lang()

        schema_name = dataset_facet_field
        #remove prefix in facet name
        schema_name = schema_name.replace('extras_', '')
        schema_name = schema_name.replace('res_extras_', '')

        # switch for dataset or resource
        if schema_name.startswith( 'res_' ):
            fields_from_schema = schema['resource_fields']
        else:
            fields_from_schema = schema['dataset_fields']

        for field in fields_from_schema:
            if field['field_name'] == schema_name:
                #if item key is given - see facet_list.html
                if default_facet_label is not None:
                    if 'choices' in field:
                        return self._get_value_from_scheming_choices_field(field['choices'], default_facet_label, language)
                    elif 'choices_helper' in field:
                        from ckantoolkit import h
                        choices_fn = getattr(h, field['choices_helper'])
                        return self._get_value_from_scheming_choices_field(choices_fn(field), default_facet_label, language)
                    else:
                        return default_facet_label;
                else:
                    if len(field['label']) > 1 and type(field['label']) is dict:
                        label_array = field['label']
                        for key, value in label_array.iteritems():
                            if key == language:
                                if value is not None:
                                    return value
                                else:
                                    return default_facet_label
                        if value is not None:
                            return value
                        else:
                            return default_facet_label
                    if field['label'] is not None:
                        return field['label']
                    else:
                        return default_facet_label


        return self._translate_facet_item_label(dataset_facet_field, default_facet_label)