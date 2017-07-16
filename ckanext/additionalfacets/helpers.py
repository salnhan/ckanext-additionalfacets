def lang():
    # access this function late in case ckan
    # is not set up fully when importing this module
    from ckantoolkit import h
    return h.lang()
