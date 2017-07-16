'''
Load either yaml or json, based on the name of the resource
'''

import json, os, inspect
from paste.reloader import watch_file

def load(f):
    if is_yaml(f.name):
        import yaml
        return yaml.load(f)
    return json.load(f)

def loads(s, url):
    if is_yaml(url):
        import yaml
        return yaml.load(s)
    return json.loads(s)

def is_yaml(n):
    return n.lower().endswith(('.yaml', '.yml'))


def load_facets_module_path(relative_path):
    '''
    Given a path like "ckanext.additionalfacets:default_facets.json"
    find the second part relative to the import path of the first
    :param relative_path: path to file
    '''

    module, file_name = relative_path.split(':', 1)

    try:
        # __import__ has an odd signature
        module_to_import = __import__(module, fromlist=[''])
    except ImportError:
        return

    file_path = os.path.join(os.path.dirname(inspect.getfile(module_to_import)), file_name)

    if os.path.exists(file_path):
        watch_file(file_path)
        return load(open(file_path))

def get_additional_facets_dict(facets_inputs):
    '''
    Get the list of facets
    :param facets_inputs: facets inputs in config
    '''
    result = {}
    for facets_input in facets_inputs:
        additional_facets = load_facets_module_path(facets_input)
        result[additional_facets['name']] = additional_facets
    return result

def get_additional_facets(facet_input):
    '''
    Get additional facets from input (single)
    '''
    return load_facets_module_path(facet_input)
