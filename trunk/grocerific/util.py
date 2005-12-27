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

#
# Import Local modules
#


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
