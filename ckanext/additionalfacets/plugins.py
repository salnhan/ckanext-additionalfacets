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
    ## configuration file
    ADDITIONAL_FACETS_CONFIG = 'ckanext.additional_facets'
    DISPLAY_FACETS_ON_GROUPS_PAGE = 'ckanext.additional_facets.display_on_group_page'
    DISPLAY_FACETS_ON_ORG_PAGE = 'ckanext.additional_facets.display_on_org_page'
    CLEAR_DEFAULT_FACETS = 'ckanext.additional_facets.clear_default_facets'

    ##fields in the json/yaml file
    DATASET_FIELD = 'dataset_field'
    DATASET_TYPE_FIELD = 'dataset_type'
    FACET_NAME_FIELD = 'facet_name'
    FACET_ITEMS_FIELD = 'facet_items'
    DEFAULT_LABEL_FIELD = 'default_label'
    NEW_LABEL_FIELD = 'new_label'

    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        facets_inputs = config.get(self.ADDITIONAL_FACETS_CONFIG, '').split()

        # get additional facets from the input
        self.additional_facets = loader.get_additional_facets(facets_inputs[0])

        self.display_facets_on_group_page = toolkit.asbool(config.get(self.DISPLAY_FACETS_ON_GROUPS_PAGE, False))
        self.display_facets_on_org_page = toolkit.asbool(config.get(self.DISPLAY_FACETS_ON_ORG_PAGE, False))
        self.clear_default_facets = toolkit.asbool(config.get(self.CLEAR_DEFAULT_FACETS, False))


    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        '''
        Insert additional facets to dataset search page
        '''
        # if no facets to insert
        if not self.additional_facets:
            return facets_dict

        # clear default facets
        if self.clear_default_facets:
            facets_dict.clear()

        facets_dict.update(self._get_facets_title_with_translation())

        return facets_dict


    def group_facets(self, facets_dict, group_type, package_type):
        '''
        Insert additional facets to group search page
        '''
        # stop if no facets to insert
        if not self.translated_additional_facets:
            return facets_dict

        if self.display_facets_on_group_page:
            facets_dict.update(self._get_facets_title_with_translation())

        return facets_dict


    def organization_facets(self, facets_dict, organization_type, package_type):
        '''
        Insert additional facets to organization search page
        '''
        # if no facets to insert
        if not self.translated_additional_facets:
            return facets_dict

        if self.display_facets_on_group_page:
           facets_dict.update(self._get_facets_title_with_translation())

        return facets_dict


    # Private methods
    def _get_facets_title_with_translation(self):
        '''
        Get the translated facet title
        '''
        # name of additional facets
        additional_facets_name = {}

        # stop if the facet list is empty
        if not self.additional_facets:
            return additional_facets_name

        # get current environment's language
        language = additional_facets_helpers.lang()

        # search and get the translated title for facet
        for facet in self.additional_facets:
            if self.DATASET_FIELD in facet and self.FACET_NAME_FIELD in facet:
                label_array = facet_item[self.FACET_NAME_FIELD]
                for key, value in label_array.iteritems():
                    if key == language and value is not None:
                         additional_facets_name[facet[self.DATASET_FIELD]] = value
                    else:
                        additional_facets_name[facet[self.DATASET_FIELD]] = facet[self.FACET_NAME_FIELD]

        return additional_facets_name


    def _translate_facet_item_label(self, dataset_facet_field, default_facet_label):
        '''
        Translate the default label of facet item. Return the default facet label if no translation available
        :param dataset_facet_field: the name of facet field in the dataset
        :param default_facet_label: the default label of the facet item
        '''

        # if facets not empty
        if self.additional_facets:
            for facet in self.additional_facets:
                # get the concrete facet
                if self.DATASET_FIELD in facet and facet[self.DATASET_FIELD] == dataset_facet_field and self.FACET_ITEMS_FIELD in facet:
                    facet_items = facet[self.FACET_ITEMS_FIELD]
                    for facet_item in facet_items:
                        # translate the label of facet
                        if facet_item[self.DEFAULT_LABEL_FIELD] == default_facet_label:
                            language = additional_facets_helpers.lang()
                            label_array = facet_item[self.NEW_LABEL_FIELD]
                            for key, value in label_array.iteritems():
                                if key == language and value is not None:
                                    default_facet_label = value

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
    # Override the parent's method
    def _get_facets_title_with_translation(self):
        '''
        Get the translated facet title
        '''
        # name of additional facets
        additional_facets_name = {}

        # stop if the facet list is empty
        if not self.additional_facets:
            return additional_facets_name

        # get current environment's language
        language = additional_facets_helpers.lang()

        # search and get the translated title for facet
        for facet in self.additional_facets:
            if self.DATASET_FIELD in facet:
                # if 'facet_name' and 'dataset_type' exist, wins the 'facet_name'
                if self.FACET_NAME_FIELD in facet:
                    label_array = facet[self.FACET_NAME_FIELD]
                    for key, value in label_array.iteritems():
                        if key == language and value is not None:
                            additional_facets_name[facet[self.DATASET_FIELD]] = value
                        else:
                            additional_facets_name[facet[self.DATASET_FIELD]] = facet[self.FACET_NAME_FIELD]
                else:
                    if facet[self.DATASET_TYPE_FIELD]:
                        from ckanext.scheming import helpers as scheming_helpers
                        package_type = self._get_dataset_type_of_facet(facet[self.DATASET_FIELD])
                        schema = scheming_helpers.scheming_get_dataset_schema(package_type)

                        if schema is None:
                            continue

                        schema_name = facet[self.DATASET_FIELD]
                        #remove prefix in facet name
                        schema_name = schema_name.replace('extras_', '')
                        schema_name = schema_name.replace('res_extras_', '')

                        # switch for dataset or resource
                        if schema_name.startswith( 'res_' ) and 'resource_fields' in schema:
                           fields_from_schema = schema['resource_fields']
                        elif 'dataset_fields' in schema:
                            fields_from_schema = schema['dataset_fields']
                        else:
                           continue

                        for field in fields_from_schema:
                            # ckanext-scheming schemas
                            if field['field_name'] == schema_name and 'label' in field:
                                additional_facets_name[facet[self.DATASET_FIELD]] = field['label']
                                label_array = field['label']
                                for key, value in label_array.iteritems():
                                    if key == language and value is not None:
                                        additional_facets_name[facet[self.DATASET_FIELD]] = value
                                    else:
                                        additional_facets_name[facet[self.DATASET_FIELD]] = field['label']

        return additional_facets_name


    def _get_dataset_type_of_facet(self, dataset_facet_field):
        '''
        Get the dataset type, which contains the facet
        :param dataset_facet_field: name of facet field in the dataset (e.g: `extras_information_category`)
        '''
        # set default dataset
        dataset_type = 'dataset'
        # if facets not empty
        if self.additional_facets:
            for facet in self.additional_facets:
                # get the concrete facet
                if self.DATASET_FIELD in facet and facet[self.DATASET_FIELD] == dataset_facet_field and self.DATASET_TYPE_FIELD in facet:
                    dataset_type = facet[self.DATASET_TYPE_FIELD]

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
                        if key == language and value is not None:
                            return value

        return default_facet_label


    def _get_facet_items_of_facet(self, dataset_facet_field, additional_facets):
        '''
        Get the facet items of a facet, which are defined in additional facets
        :param dataset_facet_field: name of facet field in the dataset (e.g: `extras_information_category`)
        :param additional_facets: list of additional facets
        '''
        if additional_facets:
            for facet in additional_facets:
                # get the concrete facet
                if self.DATASET_FIELD in facet and facet[self.DATASET_FIELD] == dataset_facet_field and self.FACET_ITEMS_FIELD in facet:
                   return facet[self.FACET_ITEMS_FIELD]


    def _get_facet_item_label_with_translation(self, dataset_facet_field, default_facet_label):
        '''
        Translate the default label of facet item. Return the default facet label if no translation available
        :param dataset_facet_field: the name of facet field in the dataset
        :param default_facet_label: the default label of the facet item
        '''
        from ckanext.scheming import helpers as scheming_helpers
        package_type = self._get_dataset_type_of_facet(dataset_facet_field)
        schema = scheming_helpers.scheming_get_dataset_schema(package_type)

        # if a facet has `facet_items` and `dataset_type`, wins `facet_items`
        if self._get_facet_items_of_facet(dataset_facet_field, self.additional_facets) is None:

            # if schema exists
            if schema is not None:
                schema_name = dataset_facet_field
                #remove prefix in facet name
                schema_name = schema_name.replace('extras_', '')
                schema_name = schema_name.replace('res_extras_', '')

                # switch for dataset or resource
                if schema_name.startswith( 'res_' ) and 'resource_fields' in schema:
                    fields_from_schema = schema['resource_fields']
                elif 'dataset_fields' in schema:
                    fields_from_schema = schema['dataset_fields']
                else:
                    return self._translate_facet_item_label(dataset_facet_field, default_facet_label)

                for field in fields_from_schema:
                    if field['field_name'] == schema_name:
                        #if item key is given - see facet_list.html
                        if default_facet_label is not None:
                            if 'choices' in field:
                                return scheming_helpers.scheming_choices_label(field['choices'], default_facet_label)
                            elif 'choices_helper' in field:
                                from ckantoolkit import h
                                choices_fn = getattr(h, field['choices_helper'])
                                return scheming_helpers.scheming_choices_label(choices_fn(field), default_facet_label)
                            else:
                                return default_facet_label;
                        else:
                            if len(field['label']) > 1 and type(field['label']) is dict:
                                label_array = field['label']
                                language = scheming_helpers.lang()
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