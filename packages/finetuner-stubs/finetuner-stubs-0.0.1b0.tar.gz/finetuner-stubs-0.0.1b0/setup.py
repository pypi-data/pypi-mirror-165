import os
import sys

from setuptools import find_packages, setup

if len(sys.argv) > 1 and 'target' in str(sys.argv):
    param = sys.argv[1]
    target = param.split('=')[1].strip()
    sys.argv.remove(param)
    if not target in ['finetuner', 'commons', 'stubs']:
        raise ValueError(
            'Finetuner target must be one of `finetuner`, `commons` or `stubs`.'
        )
else:
    target = 'finetuner'


if target == 'commons':
    # package name
    _name = 'finetuner-commons'
    _python_requires = '>=3.7.0'
    # package requirements
    try:
        with open('requirements-commons.txt', 'r') as f:
            _main_deps = f.readlines()
    except FileNotFoundError:
        _main_deps = []
    _extra_deps = {}
    _entry_points = {}
    _long_description = ''
    _packages = ['commons']
    _package_dir = {'commons': 'finetuner/commons'}
    _description = 'The finetuner-commons package provides common functionality between core and client.'
elif target == 'finetuner':
    _name = 'finetuner'
    _python_requires = '>=3.8.0'
    # package requirements
    try:
        with open('requirements.txt', 'r') as f:
            _main_deps = f.readlines()
    except FileNotFoundError:
        _main_deps = []

    try:
        with open('requirements-extra.txt', 'r') as f:
            _extra_deps = {'full': f.readlines()}
    except FileNotFoundError:
        _extra_deps = {}

    # package long description
    try:
        with open('README.md', encoding='utf8') as fp:
            _long_description = fp.read()
    except FileNotFoundError:
        _long_description = ''

    _packages = find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests'])
    _package_dir = {}
    _entry_points = {'console_scripts': ['finetuner=finetuner.runner.__main__:main']}
    _description = (
        'Finetuner allows one to tune the weights of any deep neural network for '
        'better embeddings on search tasks.'
    )
else:
    # package name
    _name = 'finetuner-stubs'
    _python_requires = '>=3.7.0'
    # package requirements
    _main_deps = []
    _extra_deps = {}
    _entry_points = {}
    _long_description = ''
    _packages = ['stubs']
    _package_dir = {'stubs': 'finetuner/runner/stubs'}

    _description = (
        'The finetuner-stubs package includes the interface of finetuner.runner.'
    )

# package metadata
_setup_requires = ['setuptools>=18.0', 'wheel']
_author = 'Jina AI'
_email = 'team-finetuner@jina.ai'
_keywords = (
    'jina neural-search neural-network deep-learning pretraining '
    'fine-tuning pretrained-models triplet-loss metric-learning '
    'siamese-network few-shot-learning'
)
_url = 'https://github.com/jina-ai/finetuner.fit/'
_download_url = 'https://github.com/jina-ai/finetuner.fit/tags'
_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3.8',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
]
_project_urls = {
    'Source': 'https://github.com/jina-ai/finetuner.fit/',
    'Tracker': 'https://github.com/jina-ai/finetuner.fit/issues',
}
_license = 'Proprietary'


# package version, finetuner and finetuner-commons share a same version.
__version__ = '0.0.0'
try:
    libinfo_py = os.path.join('finetuner', '__init__.py')
    libinfo_content = open(libinfo_py, 'r', encoding='utf8').readlines()
    version_line = [
        line.strip() for line in libinfo_content if line.startswith('__version__')
    ][0]
    exec(version_line)  # gives __version__
except FileNotFoundError:
    pass


if __name__ == '__main__':
    setup(
        name=_name,
        packages=_packages,
        package_dir=_package_dir,
        version='0.0.1-beta',
        include_package_data=True,
        description=_description,
        author=_author,
        author_email=_email,
        url=_url,
        license=_license,
        download_url=_download_url,
        long_description=_long_description,
        long_description_content_type='text/markdown',
        zip_safe=False,
        setup_requires=_setup_requires,
        install_requires=_main_deps,
        extras_require=_extra_deps,
        python_requires=_python_requires,
        classifiers=_classifiers,
        project_urls=_project_urls,
        keywords=_keywords,
        entry_points=_entry_points,
    )
