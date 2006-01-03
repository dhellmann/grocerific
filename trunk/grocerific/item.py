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

    
    @turbogears.expose()
    @requiresLogin()
    @usesTransaction()
    def edit(self, shoppingItem=None, user=None, usuallyBuy=None, **args):
        """Change an item in the database.
        """

        user_info = shoppingItem.getUserInfo(user)
        if usuallyBuy is not None:
            user_info.usuallybuy = usuallyBuy

        #
        # Assign the aisle information for this item.
        #
        for key, value in args.items():
            if key.startswith('aisle_'):
                store_id = key[6:]
                store = Store.get(store_id)
                shoppingItem.setAisle(store, value)

        controllers.flash('Changes saved')
        
        raise cherrypy.HTTPRedirect('/item/%s' % shoppingItem.id)
    edit.expose_resource = True

    
    @turbogears.expose(html="grocerific.templates.item_new")
    @requiresLogin()
    def new_form(self, user=None, name='', addToList=False, **args):
        """Form to add an item to the database.
        """
        return makeTemplateArgs(name=name,
                                addToList=addToList,
                                )

    
    @turbogears.expose(format="xml",
                       template="grocerific.templates.query_results",
                       content_type="text/xml",
                       )
    @usesLogin()
    def search(self, queryString=None, **args):
        """Search for items in the database.
        """
        items = ShoppingItem.search(queryString)
        if items is not None:
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
                       template="grocerific.templates.query_results",
                       content_type="text/xml",
                       )
    @usesLogin()
    def browse(self, firstLetter=None, **args):
        """Browse items in the database based on
        their first letter.
        """
        items = ShoppingItem.browse(firstLetter)
        if items is not None:
            item_count = items.count()
        else:
            items = []
            item_count = 0

        if where_clauses:
            select_string = ' OR '.join(where_clauses)
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
    def add(self, user=None, name='', addToList=False, shoppingListId=None, usuallyBuy=None, **args):
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
        # Update the usuallybuy info
        #
        if usuallyBuy:
            info = item.getUserInfo(user)
            info.usuallybuy = usuallyBuy

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
            raise cherrypy.HTTPRedirect('/list/%s' % shoppingListId)
        
        raise cherrypy.HTTPRedirect('/item/%s' % item.id)
