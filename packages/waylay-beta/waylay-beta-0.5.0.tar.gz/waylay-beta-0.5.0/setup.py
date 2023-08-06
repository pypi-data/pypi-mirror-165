"""waylay-beta build configuration"""
import json
from setuptools import setup, find_namespace_packages
import versioneer


with open("doc/byoml_runtimes.json", "r") as fh:
    runtimes_data = json.load(fh)

framework_extras = set()
runtime_extras = set()
runtime_requirements = {}
for runtime in runtimes_data['runtimes']:
    framework = runtime['framework']
    version = runtime['version']
    name = runtime.get('name', f'byoml-{framework}-{version}')
    runtime_extras.add(name)
    require = runtime.get('provided', [])
    runtime_requirements[name] = require
    framework_extra = f'byoml-{framework}'
    if framework_extra not in framework_extras:
        # first runtime is default for framework
        framework_extras.add(framework_extra)
        runtime_requirements[framework_extra] = require

with open("doc/dist.README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = long_description.replace('$FRAMEWORK_EXTRA_LIST', ', '.join(framework_extras))
    long_description = long_description.replace('$RUNTIME_EXTRA_LIST', ', '.join(runtime_extras))


setup(
    name='waylay-beta',
    description='beta release of the Waylay Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url='https://docs-io.waylay.io/#/api/sdk/python',
    author='Waylay',
    author_email='info@waylay.io',
    license='ISC',
    license_file='LICENSE.txt',
    packages=find_namespace_packages(),
    package_data={"waylay": ["py.typed"]},
    include_package_data=True,
    install_requires=[
        'httpx',
        'simple-rest-client',
        'appdirs',
        'python-jose',
        'pandas',
        'isodate',
        'joblib',
        'tqdm',  # progres bar
        'tenacity',
        'tabulate',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'mock',
            'pylint',
            'pycodestyle',
            'pydocstyle',
            'autopep8',
            'mypy',
            'typing-inspect',
            'types-pytz',
            'types-setuptools',
            'types-tabulate',
            'pdoc',
        ],
        'dev-3.7': [
        ],
        'dev-3.8': [
        ],
        'dev-3.9': [
        ],
        'dev-3.10': [
        ],
        ':python_version == "3.7"': [
            'typing_extensions'
        ],
        **runtime_requirements
    },
    setup_requires=[
        'setuptools-pep8',
        'PyYAML',
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "waylaycli = waylay.cli.waylaycli:main"
        ],
        "waylay_services": [
            "beta = waylay.service:SERVICES"
        ]
    }
)
