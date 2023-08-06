import pkg_resources


path = pkg_resources.resource_filename('cndvra8', 'VERSION')
__version__ = open(path).read()
