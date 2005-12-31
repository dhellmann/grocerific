#
# $Id$
#
# Copyright (c) 2005 Racemi, Inc.  All rights reserved.
#

"""

"""

#
# Import system modules
#
import cherrypy
import os
from sqlobject import *
import time
import turbogears
from turbogears import controllers

#
# Import Local modules
#
from grocerific.item import *
from grocerific.list import *
from grocerific.model import *
from grocerific.user import *
from grocerific.util import *

#
# Module
#

class Root(controllers.Root):

    @turbogears.expose(html="grocerific.templates.index")
    @usesLogin()
    def index(self, user=None, **kwds):
        """The main view, which shows a login screen.
        """
        return makeTemplateArgs(now=time.ctime(),
                                )

    #
    # Tie in another controller for user-related functions
    #
    user = UserManager()

    #
    # Tie in another controller for item-related functions
    #
    item = ItemManager()
    
    #
    # Tie in another controller for shopping list-related functions
    #
    list = ShoppingListController()
    
