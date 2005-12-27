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
from grocerific.model import *
from grocerific.user import UserManager

#
# Module
#

def makeTemplateArgs(**kwds):
    d = dict(**kwds)

    username = cherrypy.session.get('username')
    if username:
        d['session_is_logged_in'] = True
        d['session_user'] = username
    else:
        d['session_is_logged_in'] = False
        d['session_user'] = ''
        
    return d

def redirectToLogin():
    """Set up the redirect to the login screen.
    """
    cherrypy.session['login_came_from'] = cherrypy.request.browserUrl
    raise cherrypy.HTTPRedirect('/user/login_form')

def requiresLogin():
    """Returns a decorator which requires the user to be logged in,
    or redirects the user to the login page.
    """
    def decorator(func):

        def newfunc(self, *args, **kw):
            #
            # Make sure they are logged in
            #
            if not cherrypy.session.get('username'):
                redirectToLogin()

            output = func(self, *args, **kw)
            return output
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator

def usesLogin():
    """Returns a decorator which determines if the user is
    logged in and passes a User object to the decorated
    function if so.
    """
    def decorator(func):

        def newfunc(self, *args, **kw):
            #
            # Make sure they are logged in
            #
            username = cherrypy.session.get('username')
            if username:
                user = User.byUsername(username)
            else:
                user = None

            output = func(self, user=user, *args, **kw)
            return output
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator



def cleanString(s):
    """Clean up a string to make it safe to pass to SQLObject
    as a query.
    """
    for bad, good in [ ("'", ''),
                       ('"', ''),
                       (';', ''),
                       ]:
        s = s.replace(bad, good)
    return s
    
class ItemManager:
    """Controller for item-related functions.
    """

    @turbogears.expose(format="xml", content_type="text/xml")
    def findItems(self, queryString=None, **args):

        clean_query_string = cleanString(queryString)
        items = ShoppingItem.select("""shopping_item.name LIKE '%%%s%%'
        """ % clean_query_string)

        response_text = ''
        for item in items:
            response_text += '<tr><td>%s</td></tr>' % item.name
        
        return '''<ajax-response>
        <response type="element" id="query_results">
        <table>%s</table>
        </response>
        </ajax-response>
        ''' % response_text

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
    
