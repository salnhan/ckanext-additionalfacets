# ckanext-additionalfacets
Adds additional facets, which defined in json/yml file, for ckan 

ckanext-additionalfacets
========================

The extension allows to add the additional facets into the facets list
on the search page, the organzations page and the groups page without adjustment the code

You must only define you own facets in json or yaml file and link it to the ckan configuration and activate the plugin

The extension `ckanext-additionalfacets` supplies 2 plugins for displaying your own facets:

* `additional_facets` - if the extension `ckanext-scheming` is not being used (your datasets are not created by `ckanext-scheming`)
* `additional_facets_from_scheming_dataset` - if the extension `ckanext-scheming` is in being used (your datasets are created by `ckanext-scheming`)

Requirements
============

* This plugin is developed under usage of CKAN 2.5.5 Ubuntu 14.04 package.
* If the plugin `additional_facets_from_scheming_dataset` is activated, make sure, that extension `ckanext-scheming` has been installed

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
#   module-path:file to schemas being used
scheming.dataset_schemas = ckanext.addtionalfacets:scheming/basic/dataset.json

# ckanext-additionalfacets settings
## additional facets list
ckanext.additional_facets = ckanext.additionalfacets:example_facets.json

## clear default facets (true/false)
ckanext.additional_facets.clear_default_facets = true

## allows to display facets on group page (true/false)
ckanext.additional_facets.display_on_group_page = true

## allows to display facets on organization page (true/false)
ckanext.additional_facets.display_on_org_page = true

```

Example for additional facets
-----------------------------

* In json - [default facets_json](ckanext/additionalfacets/default_facets.json)
* In yaml - [default_facets_yml](ckanext/additionalfacets/default_facets.yml)



Field Keys
----------

### `facets`

The `facets` array of facet 
A facet include:

* `dataset_type` - name of dataset, which contains the facet. Given if the dataset is created the cknext-scheming
* `dataset_field` - field name in the dataset, which will be display in the CKAN facets
* `facet_name` - the title of the facet with translation
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
facets:
# facet from dataset "basic-dataset", which is generated by ckanext-scheming
- dataset_type: basic-dataset
  # field, which will be selected as facet
  dataset_field: extras_information_category
  facet_name:
    en: Information categories
    de: Informationskategorien
- dataset_type: basic-dataset
  dataset_field: extras_information_type
  facet_name:
    en: Information type
    de: Informationsgegenstand
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
    en: Authors
    de: Autoren
