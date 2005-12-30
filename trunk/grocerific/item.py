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
from turbogears import controllers

#
# Import Local modules
#
from grocerific.util import *
from grocerific.model import *
from grocerific.user import usesLogin, requiresLogin

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
    @usesLogin()
    def findItems(self, queryString=None, **args):
        """Search for items in the database.
        """
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
        return makeTemplateArgs(shopping_items=items,
                                shopping_item_count=item_count,
                                )

    @turbogears.expose(format="xml",
                       template="grocerific.templates.shopping_list",
                       content_type="text/xml")
    @usesLogin()
    def showList(self, user=None, listName='Next Trip', **kwds):
        """Show the contents of a shopping list.
        """
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

    def getActiveShoppingList(self, user):
        """Find the active shopping list for the user.
        """
        if user is None:
            return None
        shopping_lists = ShoppingList.selectBy(user=user,
                                               name='Next Trip',
                                               )
        try:
            shopping_list = shopping_lists[0]
        except IndexError:
            shopping_list = ShoppingList(name='Next Trip',
                                         user=user,
                                         )
            
        return shopping_list
    
    @turbogears.expose(format="xml", content_type="text/xml")
    @usesLogin()
    def addToList(self, user=None, itemId=None, **args):
        """Add an item to a shopping list.
        """
        try:
            item = ShoppingItem.get(itemId)
        except SQLObjectNotFound:
            controllers.flash('Unrecognized item')
            response = '<ajax-response/>'
        else:
            shopping_list = self.getActiveShoppingList(user)
            if shopping_list:
                shopping_list.add(item)

            raise cherrypy.HTTPRedirect('/item/showList')

        return response

    @turbogears.expose(format="xml", content_type="text/xml")
    @usesLogin()
    def removeFromList(self, user=None, itemId=None, **args):
        """Remove an item from a shopping list.
        """
        try:
            existing_item = ShoppingListItem.get(itemId)
        except SQLObjectNotFound:
            controllers.flash('Unrecognized item')
            response = '<ajax-response/>'
        else:
            existing_item.destroySelf()
            raise cherrypy.HTTPRedirect('/item/showList')

        return response

    @turbogears.expose(html="grocerific.templates.item_add")
    @requiresLogin()
    def add_form(self, user=None, name='', addToList=False, **args):
        """Form to add an item to the database.
        """
        return makeTemplateArgs(name=name,
                                addToList=addToList,
                                )

    @turbogears.expose()
    @requiresLogin()
    @usesTransaction()
    def add(self, user=None, name='', addToList=False, **args):
        """Add an item to the database.
        """
        name = name.strip()
        if not name:
            controllers.flash('Please enter a description of the item to add')
            raise cherrypy.HTTPRedirect('/item/add_form')

        #
        # We don't know what database layer we're going
        # to use, so we don't know what exception we
        # get when we insert a duplicate.  So, we try
        # to do a lookup before the insert to detect
        # the existing item.
        #
        try:
            # Look for existing item
            item = ShoppingItem.byName(name)
        except SQLObjectNotFound:
            # Insert the new item
            item = ShoppingItem(name=name)

        #
        # Add the item to the shopping list.
        #
        if addToList:
            shopping_list = self.getActiveShoppingList(user)
            if shopping_list:
                shopping_list.add(item)
        
        raise cherrypy.HTTPRedirect('/item/%s' % item.id)

    @turbogears.expose(html="grocerific.templates.item_edit")
    @usesLogin()
    def default(self, itemId=None, *args, **kwds):
        """Form to edit an item in the database.
        """
        item = ShoppingItem.get(itemId)
        response = makeTemplateArgs(shopping_item=item)
        return response

    @turbogears.expose()
    @requiresLogin()
    def edit(self, user=None, itemId=None, **args):
        """Change an item in the database.
        """
        item = ShoppingItem.get(itemId)
        return makeTemplateArgs(shopping_item=item)
