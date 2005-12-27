#
# $Id$
#
# Copyright (c) 2005 Racemi, Inc.  All rights reserved.
#

"""ItemManager controller

"""

#
# Import system modules
#
import turbogears

#
# Import Local modules
#
from grocerific.util import *
from grocerific.model import *

#
# Module
#

    
class ItemManager:
    """Controller for item-related functions.
    """

    @turbogears.expose(format="xml", content_type="text/xml")
    def findItems(self, queryString=None, **args):
        #
        # Clean up the string we are given and turn it
        # into words that might appear in the name
        # of a shopping item.
        #
        clean_query_string = cleanString(queryString)
        words = clean_query_string.split(' ')
        where_clauses = []
        for word in words:
            word = word.strip()
            if not word:
                continue
            where_clauses.append("shopping_item.name LIKE '%%%s%%'" % word)

        #
        # Assemble the select string and get the items.
        #
        if where_clauses:
            select_string = ' AND '.join(where_clauses)
            items = ShoppingItem.select(select_string)
        else:
            items = []

        #
        # Format the response table
        #
        response_text = ''
        for item in items:
            response_text += '<tr><td>%s</td></tr>' % item.name
        
        return '''<ajax-response>
        <response type="element" id="query_results">
        <table>%s</table>
        </response>
        </ajax-response>
        ''' % response_text
