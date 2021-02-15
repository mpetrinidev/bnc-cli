from setuptools import setup

setup(
    name="bnc",
    version="1.0",
    packages=["src", "src.commands"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        bnc=src.cli:cli
    """,
)