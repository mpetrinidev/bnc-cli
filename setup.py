import pathlib
import os

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')
bnc_package_name = os.environ.get('BNC_SETUP_PKG_NAME')

setup(
    name=bnc_package_name,  # Required (bnc or bnc_testnet)
    version=os.environ.get('BNC_SETUP_PKG_VERSION'),  # Required 0.0.1-alpha
    description='Unofficial Binance CLI to interact with Binance API',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/mpetrinidev/bnc-cli',  # Optional
    author='Mauro Petrini',  # Optional
    author_email='dev.mpetrini@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Other Audience',
        'Topic :: Terminals',
        'Topic :: Utilities',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='bnc, binance, binance-api, binance-cli, bnc-cli',  # Optional
    packages=[f'{bnc_package_name}', f'{bnc_package_name}.commands', f'{bnc_package_name}.utils',
              f'{bnc_package_name}.validation'],  # Required
    include_package_data=True,
    package_data={'': ['config.json']},
    python_requires='>=3.8, <4',
    install_requires=[
        'requests_async~=0.6.2',
        'click~=7.1.2',
        'pandas~=1.2.2',
        'PyYAML~=5.4.1',
        'jmespath~=0.10.0',
        'colorama~=0.4.4'
    ],  # Optional
    entry_points="""
        [console_scripts]
        {command}={module_prefix}.cli:entry_point
    """.format(command=bnc_package_name, module_prefix=bnc_package_name),
    project_urls={  # Optional
        'Source': 'https://github.com/mpetrinidev/bnc-cli',
        'Documentation': 'https://github.com/mpetrinidev/bnc-cli/wiki',
        'Bug Reports': 'https://github.com/mpetrinidev/bnc-cli/issues'
    }
)
