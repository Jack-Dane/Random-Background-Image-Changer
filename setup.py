
from setuptools import setup, find_packages

setup(
    name="randomBackgroundChanger",
    version="0.0.1",
    author="Jack Dane",
    author_email="jackdane@jackdane.co.uk",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask_cors",
        "flask_socketio",
        "requests",
        "sqlalchemy",
        "gunicorn",
        "greenlet",
        # https://github.com/benoitc/gunicorn/pull/2581
        # eventlet needs to be pinned due to being unable to work with gunicorn
        # fixed but not yet a release
        "eventlet==0.24.1",
        "gevent",
        "dnspython==1.16.0"
    ],
    entry_points={
        "console_scripts": [
            "startFileHandler=randomBackgroundChanger.scripts:startFileHandler",
            "addImgurPin=randomBackgroundChanger.scripts:addImgurPin",
            "updateBackgroundImage=randomBackgroundChanger.scripts:updateBackgroundImage",
            "createTables=randomBackgroundChanger.DAL.database:createTables"
        ]
    }
)
