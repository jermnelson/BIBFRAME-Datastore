__author__ = "Jeremy Nelson"
__license__ = "GPLv3"


import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, "VERSION")) as version:
    __version__ = version.read().strip()

import importlib
import asyncio
import falcon
import sys
from asyncio import subprocess
semantic_server = importlib.import_module("semantic-server.app", None)

class StartUp(object):

    def on_get():
        pass

    def on_post():
        pass

    def on_delete():
        pass

# Add BIBFRAME specific REST API
##semantic_server.api.add_route("/Work")
##semantic_server.api.add_route("/Annotation")
##semantic_server.api.add_route("/Authority")
##semantic_server.api.add_route("/Instance")

if __name__ == "__main__":
    semantic_server.main()
