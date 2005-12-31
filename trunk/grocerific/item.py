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
from rest_resource import RESTResource

#
# Module
#

    
class ItemManager(RESTResource):
    """Controller for item-related functions.
    """

    def REST_instantiate(self, itemId, **kwds):
        """Look for the item by it's primary id.
        """
        try:
            return ShoppingItem.get(itemId)
        except SQLObjectNotFound:
            return None

    def REST_create(self, *args, **kwds):
        """Create a new item?
        FIXME - Not sure when this is called.
        """
        raise NotImplementedError()


    @turbogears.expose(html="grocerific.templates.item_edit")
    @requiresLogin()
    def index(self, shoppingItem=None, user=None, **kwds):
        """Form to edit an item in the database.
        """
        response = makeTemplateArgs(shopping_item=shoppingItem,
                                    user=user,
                                    )
        return response
    index.expose_resource = True

    @turbogears.expose(html="grocerific.templates.item_new")
    @requiresLogin()
    def new_form(self, user=None, name='', addToList=False, **args):
        """Form to add an item to the database.
        """
        return makeTemplateArgs(name=name,
                                addToList=addToList,
                                )
    
    ###################

    @turbogears.expose(format="xml",
                       template="grocerific.templates.query_results",
                       content_type="text/xml",
                       )
    @usesLogin()
    def search(self, queryString=None, **args):
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

    @turbogears.expose()
    @requiresLogin()
    @usesTransaction()
    def add(self, user=None, name='', addToList=False, shoppingListId=None, **args):
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
        if addToList and shoppingListId:
            try:
                shopping_list = ShoppingList.get(shoppingListId)
            except SQLObjectNotFound:
                pass
            else:
                shopping_list.add(item)
        
        raise cherrypy.HTTPRedirect('/item/%s' % item.id)

    @turbogears.expose()
    @requiresLogin()
    def edit(self, user=None, itemId=None, **args):
        """Change an item in the database.
        """
        item = ShoppingItem.get(itemId)
        return makeTemplateArgs(shopping_item=item)
