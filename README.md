# ckanext-additionalfacets
Adds additional facets (in json) for ckan 

ckanext-additionalfacets
========================

The extension allows to add the additional facets into the facets list
on the search page, the organzations page and the groups page


Requirements
============

This plugin is developed under usage of CKAN 2.5.5 Ubuntu 14.04 package.
It requires ckanext-scheming.

Installation
============


```{r, engine='bash', install_ckanext-additionalfacets}
    ./usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/
    pip install -e 'git+https://github.com/salnhan/ckanext-additionalfacets.git#egg=ckanext-additionalfacets'
    deactivate
```

Configuration
=============

Set the schemas you want to use with configuration options (ckans .ini file) and activate the search for all packages by default:

```ini

# activate plugin additional_facets
ckan.plugins = additional_facets

# ckanext-additionalfacets settings
## additional facets list
ckanext.additional_facets = ckanext.additionalfacets:default_facets.json
## allows to display facets on group page (true/false)
additional_facets.display_on_group_page = true
## allows to display facets on organization page (true/falese)
ckanext.additional_facets.display_on_org_page = true

```

Example for additional facets in json
-----------------------

* [default facets](ckanext/additionalfacets/default_facets.json)


Field Keys
----------

### `facets`

The `facets` array of facet 
A facet include:

* `dataset_field` - field name in the dataset, which will be display in the CKAN facets
* `facet_name` - the title of the facet with translation
* `facet_items`- (optional) to be used in order to translate the label of the facet items

Translation for a facet title
-----------------------------
```json
{
  "dataset_field": "extras_information_category",
  "facet_name": {
    "en": "Information categories",
    "de": "Informationskategorien"
  }
}
```

Translation for a facet item
-----------------------------
```json
{
  "dataset_field": "extras_information_category",
  "facet_name": {
        "en": "Information categories",
        "de": "Informationskategorien"
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
      "default_label": "Bildung & Wissenschaft",
      "new_label": {
        "en": "Education & Economy",
        "de": "Bildung & Wissenschaft"
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
```