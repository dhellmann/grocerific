#
# $Id: init.el,v 1.6 2005/07/11 14:27:19 dhellmann Exp $
#
# Copyright (c) 2005 Racemi, Inc.  All rights reserved.
#

"""ListManager controller

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

NEXT_TRIP = 'Next Trip'


class ShoppingListController(RESTResource):
    """Controller for shopping list-related functions.
    """

    def REST_instantiate(self, listId, **kwds):
        """Look for the list by it's primary id.
        """
        try:
            return ShoppingList.get(listId)
        except:
            return None

    def REST_create(self, *args, **kwds):
        """Create a new list?
        FIXME - Not sure when this is called.
        """
        raise NotImplementedError()


    
    @requiresLogin()
    @turbogears.expose(html="grocerific.templates.shopping_list_html")
    def index(self, shoppingList=None, user=None, **kwds):
        """Show the contents of a shopping list in a full-page
        HTML format that lets the user find items and edit the list.
        """
        if shoppingList is None:
            #
            # Look for the user's 'Next Trip' shopping list
            # and redirect to that.
            #
            lists = ShoppingList.selectBy(user=user,
                                          name=NEXT_TRIP,
                                          )
            try:
                shopping_list = lists[0]
            except IndexError:
                shopping_list = ShoppingList(user=user,
                                             name=NEXT_TRIP,
                                             )
            raise cherrypy.HTTPRedirect('/list/%s' % shopping_list.id)

        #
        # Otherwise, set up the arguments for our template so
        # we can display the shoppingList contents.
        #
        return makeTemplateArgs(shopping_list=shoppingList,
                                shopping_list_items=shoppingList.getItems(),
                                )
    index.expose_resource = True

    

    @requiresLogin()
    @turbogears.expose(format="xml",
                       template="grocerific.templates.shopping_list_xml",
                       content_type="text/xml")
    def xml(self, shoppingList, user=None, **kwds):
        """Returns an AJAX-ready XML version of the list contents.
        """
        return makeTemplateArgs(shopping_list=shoppingList, 
                                shopping_list_items=shoppingList.getItems(),
                                )
    xml.expose_resource = True



    @requiresLogin()
    @turbogears.expose(format="xml",
                       template="grocerific.templates.shopping_list_xml",
                       content_type="text/xml")
    def update(self, shoppingList, itemId=None, newQuantity=None, user=None, **kwds):
        """Change the quantity of an item in the list.
        """
        to_update = ShoppingListItem.get(itemId)
        to_update.quantity = newQuantity
        return makeTemplateArgs(shopping_list=shoppingList, 
                                shopping_list_items=shoppingList.getItems(),
                                )
    update.expose_resource = True


    
    @requiresLogin()
    @turbogears.expose(format="xml",
                       content_type="text/xml")
    def remove(self, shoppingList, itemId=None, user=None, **kwds):
        """Remove an item from a shopping list.
        """
        try:
            existing_item = ShoppingListItem.get(itemId)
        except SQLObjectNotFound:
            controllers.flash('Unrecognized item')
            response = '<ajax-response/>'
        else:
            existing_item.destroySelf()
            raise cherrypy.HTTPRedirect('/list/%s/xml' % shoppingList.id)

        return response
    remove.expose_resource = True


    
    @requiresLogin()
    @turbogears.expose(format="xml",
                       content_type="text/xml")
    def add(self, shoppingList, itemId=None, user=None, **kwds):
        """Add an item to a shopping list.
        """
        try:
            item = ShoppingItem.get(itemId)
        except SQLObjectNotFound:
            controllers.flash('Unrecognized item')
            response = '<ajax-response/>'
        else:
            shoppingList.add(item)

            raise cherrypy.HTTPRedirect('/list/%s/xml' % shoppingList.id)

        return response
    add.expose_resource = True
    
