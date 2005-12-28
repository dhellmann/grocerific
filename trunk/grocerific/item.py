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

    @turbogears.expose(format="xml",
                       template="grocerific.templates.query_results",
                       content_type="text/xml",
                       )
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
            item_count = items.count()
        else:
            items = []
            item_count = 0

        #
        # Format the response table
        #
        return makeTemplateArgs(items=items,
                                item_count=item_count,
                                )

    @turbogears.expose(format="xml",
                       template="grocerific.templates.shopping_list",
                       content_type="text/xml")
    @usesLogin()
    def showList(self, user=None, listName='Next Trip', **kwds):
        #
        # Find the active shopping list
        #
        shopping_lists = ShoppingList.selectBy(user=user,
                                               name='Next Trip',
                                               )
        try:
            shopping_list = shopping_lists[0]
        except IndexError:
            shopping_list = None
            shopping_list_items = None
        else:
            shopping_list_items = shopping_list.getItems()
            
        return makeTemplateArgs(shopping_list=shopping_list,
                                shopping_list_items=shopping_list_items,
                                )

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

            raise cherrypy.HTTPRedirect('/item/showList')

        return response

    @turbogears.expose(format="xml", content_type="text/xml")
    @usesLogin()
    def removeFromList(self, user=None, itemId=None, **args):
        try:
            existing_item = ShoppingListItem.get(itemId)
        except SQLObjectNotFound:
            controllers.flash('Unrecognized item')
            response = '<ajax-response/>'
        else:
            existing_item.destroySelf()
            raise cherrypy.HTTPRedirect('/item/showList')

        return response
