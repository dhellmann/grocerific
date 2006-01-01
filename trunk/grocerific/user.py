#
# $Id$
#
# Copyright (c) 2005 Racemi, Inc.  All rights reserved.
#

"""The UserManager controller.

"""

#
# Import system modules
#
import cherrypy
from sqlobject import *
import turbogears
from turbogears import controllers

#
# Import Local modules
#
from grocerific.model import *
from grocerific.util import *

#
# Module
#


def redirectToLogin():
    """Set up the redirect to the login screen.
    """
    cherrypy.session['login_came_from'] = cherrypy.request.browserUrl
    raise cherrypy.HTTPRedirect('/user/login_form')

def getUserForSession():
    """Checks the session and cookie settings and returns
    a User if there is a user logged in.
    """
    user = None
    
    #
    # Look for a logged-in session
    #
    username = cherrypy.session.get('username')
    if username:
        user = User.byUsername(username)

    else:
        #
        # Look for a rememberme cookie
        #
        rememberme = cherrypy.request.simpleCookie.get('rememberme')
        if rememberme is not None:
            rememberme = rememberme.value
            username, hash = rememberme.split(' ')
            user = User.byUsername(username)
            expected_cookie = user.getRememberMeCookieValue()

            if rememberme == expected_cookie:
                setUpSessionLogin(user)
            else:
                # Reset to None if the values don't
                # match.  Otherwise, we've already
                # loaded our user object.
                user = None
    return user

def requiresLogin():
    """Returns a decorator which requires the user to be logged in,
    or redirects the user to the login page.
    """
    def decorator(func):

        def newfunc(self, *args, **kw):
            #
            # Make sure they are logged in
            #
            user = getUserForSession()
            if not user:
                redirectToLogin()
            #print 'LOGGED IN AS', user

            output = func(self, user=user, *args, **kw)
            return output
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator

def setUpSessionLogin(user):
    """Set up the user information in the session.
    """
    if user is not None:
        cherrypy.session['username'] = user.username
        cherrypy.session['userid'] = user.id
    else:
        try:
            del cherrypy.session['username']
        except KeyError:
            pass
        try:
            del cherrypy.session['userid']
        except KeyError:
            pass
    return


def usesLogin():
    """Returns a decorator which determines if the user is
    logged in and passes a User object to the decorated
    function if so.
    """
    def decorator(func):

        def newfunc(self, *args, **kw):
            user = getUserForSession()
            output = func(self, user=user, *args, **kw)
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
        # Clear the username and password from the session
        #
        username = cherrypy.session.get('username')
        if username:
            #
            # Clear the session login
            #
            setUpSessionLogin(None)

            #
            # Remove the user cookie
            #
            cherrypy.response.simpleCookie['rememberme'] = username
            cherrypy.response.simpleCookie['rememberme']['path'] = '/'
            cherrypy.response.simpleCookie['rememberme']['max-age'] = 0
            
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
        setUpSessionLogin(userobj)

        #
        # Store information about this user in a cookie
        # so we remember them the next time they come back,
        # even if their session has expired.
        #
        if not cherrypy.request.simpleCookie.get('rememberme'):
            cherrypy.response.simpleCookie['rememberme'] = userobj.getRememberMeCookieValue()
            cherrypy.response.simpleCookie['rememberme']['path'] = '/'
        
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

    @turbogears.expose()
    def index(self):
        raise cherrypy.HTTPRedirect('/user/prefs')

    @requiresLogin()
    @turbogears.expose(html="grocerific.templates.prefs")
    def prefs(self, user):
        """Form to register a new user.
        """
        return makeTemplateArgs(username=user.username,
                                password=user.password,
                                email=user.email,
                                )

    @turbogears.expose()
    def edit_prefs(self, password, email=None, **kwds):
        """Register a new user.
        """
        try:
            user = User.get(cherrypy.session.get('userid'))
        except SQLObjectNotFound:
            redirectToLogin()
            
        user.password = password
        user.email = email
        cherrypy.session['login_came_from'] = '/user/prefs'
        return self.login(user.username, password)
