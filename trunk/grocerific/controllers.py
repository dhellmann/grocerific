#
# $Id: init.el,v 1.6 2005/07/11 14:27:19 dhellmann Exp $
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
        #
        # Get the user's "Next Trip" list.
        #
        if user is not None:
            # Try to find the list
            shopping_lists = ShoppingList.selectBy(user=user,
                                                   name='Next Trip',
                                                   )
            try:
                shopping_list = shopping_lists[0]
            except IndexError:
                # Create a new list
                shopping_list = ShoppingList(user=user, name='Next Trip')
            items = shopping_list.getItems()
            empty_list = not items.count()
        else:
            shopping_list = None
            empty_list = True
            items = []
            
        return makeTemplateArgs(now=time.ctime(),
                                shopping_list=shopping_list,
                                empty_list=empty_list,
                                )

    #
    # Tie in another controller for user-related functions
    #
    user = UserManager()

    #
    # Tie in another controller for item-related functions
    #
    item = ItemManager()
    
