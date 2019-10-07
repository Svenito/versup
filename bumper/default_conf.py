default_conf = {
    'version': {
        'enabled': True, # Bump the version number
        'initial': '0.0.0', # Initial version
        'increments': ['major', 'minor', 'patch', 'premajor', 'preminor', 'prepatch', 'prerelease', 'custom'] # List of available increments to pick from
    }
}