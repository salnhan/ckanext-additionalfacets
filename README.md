# ckanext-additionalfacets
Adds additional facets with tranlation, which are defined in json/yml file, for ckan without coding.

ckanext-additionalfacets
========================

The extension allows to add the additional facets into the facets list
on the search page, the organzations page and the groups page without adjustment the code.

To add the new additional facets you must only define you own facets in json or yaml file and link it to the ckan configuration and activate the plugin.

The extension `ckanext-additionalfacets` provides 2 plugins for creating and displaying your own facets:

* `additional_facets` - if the extension `ckanext-scheming` is not being used (your meta data schemas are not created by `ckanext-scheming`)
* `additional_facets_from_scheming_dataset` - if the extension `ckanext-scheming` is in being used (your meta data schemas are created by `ckanext-scheming`) (recommend)

Requirements
============

* This plugin is developed under usage of CKAN 2.5.5 Ubuntu 14.04 package.
* If you activate the plugin `additional_facets_from_scheming_dataset`, make sure, that extension `ckanext-scheming` has been installed

Installation
============


```{r, engine='bash', install_ckanext-scheming}
    ./usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/
    pip install -e 'git+https://github.com/ckan/ckanext-scheming.git#egg=ckanext-scheming'
    cd /usr/lib/ckan/default/src/ckanext-spatial/
    pip install -r pip-requirements.txt
    #python setup.py develop
    deactivate
```

```{r, engine='bash', install_ckanext-additionalfacets}
    ./usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/
    pip install -e 'git+https://github.com/salnhan/ckanext-additionalfacets.git#egg=ckanext-additionalfacets'
    pip install -r requirements.txt
    deactivate
```

Configuration
=============

Set the schemas you want to use with configuration options (ckans .ini file) and activate the search for all packages by default:

```ini

# activate plugin `additional_facets` if the ckanext-scheming is not in use
ckan.plugins = additional_facets

# activate plugin `additional_facets_from_scheming_dataset` if the ckanext-scheming is in use
ckan.plugins = scheming_datasets additional_facets_from_scheming_dataset
# module-path:file to schemas being used
scheming.dataset_schemas = ckanext.addtionalfacets:scheming/basic/dataset.json

# ckanext-additionalfacets settings
## additional facets list
ckanext.additional_facets = ckanext.additionalfacets:example_facets.json

## clear current default facets and show only the your own facets (true/false)
ckanext.additional_facets.clear_default_facets = true

## allows to display facets on group page (true/false)
ckanext.additional_facets.display_on_group_page = true

## allows to display facets on organization page (true/false)
ckanext.additional_facets.display_on_org_page = true

```

Example for additional facets
-----------------------------

* In json - [example facets_json](ckanext/additionalfacets/example_facets.json)
* In yaml - [example_facets_yml](ckanext/additionalfacets/example_facets.yml)

Example for meta data schema, which is created with ckanext-scheming
-----------------------------------------------------------

* [dataset_json](ckanext/additionalfacets/scheming/basic/dataset.json)

Additional facets are field `information_category` and `registerobject_type` from this schema

Field Keys
----------

### `facets`

The `facets` array of facet 
A facet include:

* `dataset_type` - name of dataset, which contains the facet. Given if the dataset is created the cknext-scheming
* `dataset_field` - field name in the dataset, which will be display in the CKAN facets
* `facet_name` - the title of the facet with translation, if `dataset_type` exists and the title of this field should like as the field in the dataset,
you don't need to add this field, otherwise the title in `facet_name` will be display in frontend
* `facet_items`- (optional) contains the translation of label of facet items. This field will not be considered, if `dataset_type` is given 
* `default_label` - current label of the facet item
* `new_label` - new label of the facet item with translation


Title of a additional facet in json with translation
----------------------------------------------------
```json
{
  "dataset_field": "extras_information_category",
  "facet_name": {
    "en": "Information categories",
    "de": "Informationskategorien"
  }
}
```

Additional facet item in json with translation not using ckanext-scheming
-------------------------------------------------------------------------
```json
{
  "facets": [
    {
      "dataset_field": "groups",
      "facet_name": {
        "en": "Group",
        "de": "Gruppe"
      },
      "facet_items": [
        {
          "default_label": "Bauen & Wohnen",
          "new_label": {
            "en": "Build & Live",
            "de": "Bauen & Wohnen"
          }
        },
        {
          "default_label": "Wirtschaft und Arbeit",
          "new_label": {
            "en": "Economy & Job",
            "de": "Wirtschaft und Arbeit"
          }
        },
        {
          "default_label": "natur_umwelt",
          "new_label": {
            "en": "Nature & Environment",
            "de": "Natur & Umwelt"
          }
        }
      ]
    }
  ]
}
```

Additional facet item in json with translation using ckanext-scheming
-------------------------------------------------------------------------
```json
{
  "facets": [
    {
      "dataset_type": "basic-dataset",
      "dataset_field": "extras_information_category",
      "facet_name": {
        "en": "Information categories",
        "de": "Informationskategorien"
      }
    }
  ]
}
```

Additional facet items in json with translation (mixing)
---------------------------------------------------
```json
{
  "facets": [
    {
      "dataset_type": "basic-dataset",
      "dataset_field": "extras_information_category",
      "facet_name": {
        "en": "Information categories",
        "de": "Informationskategorien"
      }
    },
    {
      "dataset_type": "basic-dataset",
      "dataset_field": "extras_registerobject_type"
    },
    {
      "dataset_field": "groups",
      "facet_name": {
        "en": "Group",
        "de": "Gruppe"
      },
      "facet_items": [
        {
          "default_label": "Bauen & Wohnen",
          "new_label": {
            "en": "Build & Live",
            "de": "Bauen & Wohnen"
          }
        },
        {
          "default_label": "Wirtschaft und Arbeit",
          "new_label": {
            "en": "Economy & Job",
            "de": "Wirtschaft und Arbeit"
          }
        },
        {
          "default_label": "natur_umwelt",
          "new_label": {
            "en": "Nature & Environment",
            "de": "Natur & Umwelt"
          }
        }
      ]
    },
    {
      "dataset_field": "author",
      "facet_name": {
        "en": "Author",
        "de": "Autor"
      }
    }
  ]
}
```

Additional facet items in yaml with translation
-----------------------------------------------
```yml
- dataset_type: basic-dataset
  dataset_field: extras_information_category
  facet_name:
    en: Information categories
    de: Informationskategorien
- dataset_type: basic-dataset
  dataset_field: extras_registerobject_type
- dataset_field: groups
  facet_name:
    en: Group
    de: Gruppe
  facet_items:
  - default_label: Bauen & Wohnen
    new_label:
      en: Build & Live
      de: Bauen & Wohnen
  - default_label: Wirtschaft und Arbeit
    new_label:
      en: Economy & Job
      de: Wirtschaft und Arbeit
  - default_label: natur_umwelt
    new_label:
      en: Nature & Environment
      de: Natur & Umwelt
- dataset_field: author
  facet_name:
    en: Author
    de: Autor
```

Avoid splitting of field values in faceted search in Solr
---------------------------------------------------------
After inserting additional facets, which are not configured in the schema.xml, the value of the facet
will be split to sub values. And these sub values will be displayed as facet items of a facet

Example: The Facet's value `Energy & Climate` will be split to `energy`, `climate`, ` eneryclimate` 

If you don't want to see sub values of the facet in frontend, just insert the additional facet fields into the schema.xml of Solr as follow

```xml
<schema>
    .....
    <fields>
        <field>
                .....
                <field name="extras_information_category" type="string" indexed="true" stored="true" multiValued="true"/>
                <field name="extras_registerobject_type" type="string" indexed="true" stored="true" multiValued="true"/>
                .....
        </field>
     </fields>
     .....
     <copyField source="extras_registerobject_type" dest="text"/>
     <copyField source="extras_information_category" dest="text"/>
     ......
</schema>
```

See [example_schema_xml](ckanext/additionalfacets/solr/example_schema.xml) 
