#
# $Id$
#
# Copyright (c) 2005 Racemi, Inc.  All rights reserved.
#

"""Utility functions

"""

#
# Import system modules
#
import cherrypy
import turbogears

#
# Import Local modules
#
from grocerific.model import hub

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

def usesTransaction():
    """Returns a decorator which manages a database transaction
    when a method needs to make multiple changes to the database.
    """
    def decorator(func):

        def newfunc(self, *args, **kw):
            hub.begin()
            try:
                try:
                    output = func(self, *args, **kw)
                except cherrypy.HTTPRedirect:
                    hub.commit()
                    raise
                except:
                    hub.rollback()
                    raise
                else:
                    hub.commit()
            finally:
                hub.end()
            return output
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator
