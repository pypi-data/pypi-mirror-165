from setuptools import setup, find_packages

config = {
    "name": "saysynth",
    "version": "0.0.94",
    "packages": find_packages(),
    "package_data": {
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.yml"],
    },
    "install_requires": [
        "charset-normalizer",
        "click",
        "mido",
        "midi-utils",
        "pyyaml",
        "g2p_en",
        "nltk",
    ],
    "author": "Brian Abelson",
    "author_email": "hey@gltd.email",
    "description": "A synthesizer built on say",
    "url": "http://globally.ltd",
    "entry_points": {
        "console_scripts": ["saysynth=saysynth.cli:main", "sy=saysynth.cli:main"]
    },
}

setup(**config)
