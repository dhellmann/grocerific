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


class UserManager:
    """Controller for user operations.
    """
        
    @turbogears.expose(html="grocerific.templates.login")
    def login_form(self):
        return makeTemplateArgs()

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
        try:
            del cherrypy.session['login_came_from']
        except KeyError:
            pass
        raise cherrypy.HTTPRedirect(go_back_to)

    @turbogears.expose(html="grocerific.templates.userlist")
    def userlist(self):
        """List the users
        """
        return makeTemplateArgs(users=User.select(LIKE(User.q.username, "%")),
                                )

    @turbogears.expose(html="grocerific.templates.registration_form")
    def registration_form(self):
        """Form to register a new user.
        """
        return makeTemplateArgs()

    @turbogears.expose()
    def register(self, username, password, email=None, **kwds):
        """Register a new user.
        """
        new_user = User(username=username,
                        password=password,
                        email=email,
                        )
        return self.login(username, password)

    @turbogears.expose(html="grocerific.templates.prefs")
    def prefs(self):
        """Form to register a new user.
        """
        try:
            user = User.byUsername(cherrypy.session.get('username'))
        except SQLObjectNotFound:
            redirectToLogin()
            
        return makeTemplateArgs(username=user.username,
                                password=user.password,
                                email=user.email,
                                )

    @turbogears.expose()
    def edit_prefs(self, username, password, email=None, **kwds):
        """Register a new user.
        """
        try:
            user = User.byUsername(username)
        except SQLObjectNotFound:
            redirectToLogin()
            
        user.password = password
        user.email = email
        cherrypy.session['login_came_from'] = '/user/prefs'
        return self.login(username, password)

class Root(controllers.Root):

    @turbogears.expose(html="grocerific.templates.index")
    def index(self):
        """The main view, which shows a login screen.
        """
        return makeTemplateArgs(now=time.ctime(),
                                )
    
    user = UserManager()
