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

#
# Module
#

def sessionIsLoggedIn():
    """Returns boolean indicating whether or not the current
    session is for a user who has logged in.
    """
    username=cherrypy.session.get('username')
    if username is None:
        return False
    return True

def requiresLogin():
    """Returns a decorator which requires the user to be logged in,
    or redirects the user to the login page.
    """
    def decorator(func):

        def newfunc(self, *args, **kw):
            #
            # Make sure they are logged in
            #
            if not sessionIsLoggedIn():
                cherrypy.session['login_came_from'] = cherrypy.request.browserUrl
                raise cherrypy.HTTPRedirect('/user/login_form')

            output = func(self, *args, **kw)
            return output
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator


class UserManager:
    """Controller for user operations.
    """
        
    @turbogears.expose(html="grocerific.templates.login")
    def login_form(self):
        return dict()

    @turbogears.expose()
    def logout(self, **kwds):
        """Remove the username info from the current session.
        """
        #
        # Store the username and password in the session
        #
        del cherrypy.session['username']
        del cherrypy.session['password']
        
        #
        # Go back to the page that sent us here
        #
        raise cherrypy.HTTPRedirect('/')
        

    @turbogears.expose()
    def login(self, username=None, password=None, loginBtn=None, **kwds):
        #
        # Validate the inputs to make sure they are present
        #
        if not username:
            controllers.flash('You must enter your Username')
            raise cherrypy.HTTPRedirect('login_form')
        elif not password:
            controllers.flash('You must enter your Password')
            raise cherrypy.HTTPRedirect('login_form')

        #
        # Try to find that user
        #
        try:
            userobj = User.byUsername(username)
        except SQLObjectNotFound:
            controllers.flash('Invalid username or password')
            raise cherrypy.HTTPRedirect('login_form')

        #
        # Check the password
        #
        if userobj.password != password:
            controllers.flash('Invalid username or password')
            raise cherrypy.HTTPRedirect('login_form')

        #
        # Store the username and password in the session
        #
        cherrypy.session['username'] = username
        cherrypy.session['password'] = password
        
        #
        # Go back to the page that sent us here
        #
        go_back_to = cherrypy.session.get('login_came_from', '/')
        raise cherrypy.HTTPRedirect(go_back_to)

    @turbogears.expose(html="grocerific.templates.userlist")
    def userlist(self):
        """List the users
        """
        return dict(users=User.select(LIKE(User.q.username, "%")),
                    )

class Root(controllers.Root):

    @turbogears.expose(html="grocerific.templates.index")
    def index(self):
        """The main view, which shows a login screen.
        """
        return dict(now=time.ctime(),
                    session_is_logged_in=sessionIsLoggedIn(),
                    )
    
    user = UserManager()
