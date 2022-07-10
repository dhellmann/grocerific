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

class IndexCounter:
    def __init__(self):
        self.current = 0
        return

    def __getattr__(self, name):
        if name == 'next':
            self.current += 1
            return self.current
        raise AttributeError(name)

    

def makeTemplateArgs(**kwds):
    d = dict(**kwds)

    d['tabindex'] = IndexCounter()

    username = cherrypy.session.get('username')
    if username:
        d['session_is_logged_in'] = True
        d['session_user'] = username
    else:
        d['session_is_logged_in'] = False
        d['session_user'] = ''
        
    return d


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
