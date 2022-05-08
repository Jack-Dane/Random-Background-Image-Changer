
from setuptools import setup, find_packages

setup(
    name="randomBackgroundChanger",
    version="0.0.1",
    author="Jack Dane",
    author_email="jackdane@jackdane.co.uk",
    packages=find_packages(),
    requires=[
        "flask",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "startFileHandler=randomBackgroundChanger.scripts:startFileHandler",
            "updateBackgroundImage=randomBackgroundChanger.scripts:updateBackgroundImage"
        ]
    }
)
