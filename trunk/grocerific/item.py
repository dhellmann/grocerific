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
from grocerific.user import usesLogin

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
            #
            # Skip short words to avoid the user searching
            # for 'a' and sucking down the entire database.
            #
            if len(word) < 3:
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
            response_text += '<div class="query_result"><a class="action_link" title="Add to list" onclick="addToList(%s)">+</a> %s</div>' % \
                             (item.id, item.name)
        
        return '''<ajax-response>
        <response type="element" id="query_results">
        %s
        </response>
        </ajax-response>
        ''' % response_text

    @turbogears.expose(format="xml", content_type="text/xml")
    @usesLogin()
    def addToList(self, user=None, itemId=None, **args):
        try:
            item = ShoppingItem.get(itemId)
        except SQLObjectNotFound:
            controllers.flash('Unrecognized item')
            response = '<ajax-response/>'
        else:
            #
            # Find the active shopping list
            #
            shopping_lists = ShoppingList.selectBy(user=user,
                                                   name='Next Trip',
                                                   )
            shopping_list = shopping_lists[0]

            #
            # Make sure the item isn't already in the list
            # before adding it.
            #
            existing_items = ShoppingListItem.selectBy(list=shopping_list,
                                                       item=item,
                                                       )
            if existing_items.count() == 0:
                shopping_list_item = ShoppingListItem(list=shopping_list,
                                                      item=item,
                                                      quantity='1',
                                                      )

            #
            # Build a representation of the new list contents
            #
            items = shopping_list.getItems()
            items_string = ''
            for item in items:
                items_string += '''
                <tr class="list_item">
                  <td>%s</td>
                  <td>%s</td>
                </tr>
                ''' % (item.item.name, item.quantity)
            
            response = '''<ajax-response>
            <response type="element" id="shopping_list">
            <table width="100%%">
            %s
            </table>
            </response>
            </ajax-response>
            ''' % items_string

        return response
