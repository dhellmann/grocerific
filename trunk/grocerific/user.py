#
# $Id: init.el,v 1.6 2005/07/11 14:27:19 dhellmann Exp $
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


#
# Module
#


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
        try:
            del cherrypy.session['username']
        except KeyError:
            pass
        try:
            del cherrypy.session['password']
        except KeyError:
            pass
        
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
        cherrypy.session['userid'] = userobj.id
        
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
        userid = cherrypy.session.get('userid')
        if userid:
            try:
                user = User.get(userid)
            except SQLObjectNotFound:
                redirectToLogin()
        else:
            redirectToLogin()
                
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
