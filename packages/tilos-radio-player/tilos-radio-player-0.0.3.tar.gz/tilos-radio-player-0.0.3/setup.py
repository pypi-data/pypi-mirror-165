from importlib.metadata import entry_points
from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Tilos Rádió Player'
LONG_DESCRIPTION = 'Tilos Player unofficial lets you play your favourite Tilos Rádió shows in an instant'

requirements = ["certifi==2022.5.18.1", "charset-normalizer==2.0.12", "idna==3.3",
                "requests==2.28.0", "simple-term-menu==1.4.1", "urllib3==1.26.9"]

# Setting up    
setup(
    name="tilos-radio-player",
    version=VERSION,
    author="xa49",
    author_email="<tilosplayer@gmail.com>",
    readme="README.md",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={"console_scripts": ["tilos=tilos_radio_player.tilos_interactive:main"]},
    install_requires=requirements,
    keywords=['python'],
    classifiers=[
    ]
)