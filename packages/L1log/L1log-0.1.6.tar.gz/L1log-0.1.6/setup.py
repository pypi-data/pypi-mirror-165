import setuptools
import os.path

setupdir = os.path.dirname(__file__)

REQUIREMENTS = ["thonny>=3.3.13"]
VERSION = "0.1.6"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="L1log",
    version=VERSION,
    author="Yvan PETER, MiRabelle NEBUT, Corentin DUVIVIER",
    author_email="mirabelle.nebut@univ-lille.fr, yvan.peter@univ-lille.fr,corentin.duvivier.etu@univ-lille.fr",
    description="A plugin that logs and send all the user's actions to an LRS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.univ-lille.fr/mirabelle.nebut/thonny-logs",
    project_urls={
    },
    platforms=["Windows", "macOS", "Linux"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "thonnycontrib": ["*.py"],
        "thonnycontrib.thonny_LoggingPlugin": ["*.py"],
        "thonnycontrib.thonny_LoggingPlugin.utils": ["*.py"],
        "thonnycontrib.thonny_LoggingPlugin.configuration": ["*.py"],
        "thonnycontrib.thonny_LoggingPlugin.communication": ["*.py"],
        "thonnycontrib.thonny_LoggingPlugin.formats": ["*.py"],
        "thonnycontrib.thonny_LoggingPlugin.processing": ["*.py"],
    },
    packages=[  
        "thonnycontrib",
        "thonnycontrib.thonny_LoggingPlugin",
        "thonnycontrib.thonny_LoggingPlugin.utils",
        "thonnycontrib.thonny_LoggingPlugin.processing",
        "thonnycontrib.thonny_LoggingPlugin.formats",
        "thonnycontrib.thonny_LoggingPlugin.communication",
        "thonnycontrib.thonny_LoggingPlugin.configuration",
    ],
    install_requires=REQUIREMENTS,
    python_requires=">=3.6",
)
