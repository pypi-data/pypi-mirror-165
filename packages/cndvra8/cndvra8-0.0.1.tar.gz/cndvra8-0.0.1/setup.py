from setuptools import setup, find_packages
from cndvra8.__version__ import __version__

setup(name='cndvra8',
    version=__version__,
    description="The definitive tools to manage vra8 from API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='',
    author='Denis FABIEN',
    author_email='denis.fabien@changendevops.com',
    url='https://changendevops.com',
    license='MIT/X11',
    packages=find_packages(exclude=['ez_setup', 'examples', 'spec', 'spec.*']),
    include_package_data=True,
    package_data={'cndvra8': ['VERSION']},
    zip_safe=False,
    project_urls={
        "Documentation": "https://changendevops.com",
        "Source": "https://gitlab.com/changendevops/cndvra8",
    },
)