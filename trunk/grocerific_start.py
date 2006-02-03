#!/usr/bin/env python
#
# For use with mod_python
#
import pkg_resources
pkg_resources.require("TurboGears")

import cherrypy
from os.path import *
import sys

def mp_setup():
    """mpcp.py looks for this method for CherryPy configus bug our *.cfg
    files handle that
    """
    return

# first look on the command line for a desired config file,
# if it's not on the command line, then
# look for setup.py in this directory. If it's not there, this script is
# probably installed
#if len(sys.argv) > 1:
#    cherrypy.config.update(file=sys.argv[1])
#elif exists(join(dirname(__file__), "setup.py")):
#    cherrypy.config.update(file="dev.cfg")
#else:
#    cherrypy.config.update(file="prod.cfg")
cherrypy.config.update(file=os.path.join(os.path.dirname(__file__), 'homer_dev.cfg'))

from grocerific.controllers import Root

cherrypy.root = Root()

if __name__ == '__main__':
    cherrypy.server.start()
