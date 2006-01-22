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
        except SQLObjectNotFound:
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
        # Figure out what shopping lists we have that we could
        # copy into this one.  The list is limited to those
        # that have some items and are not the same list as
        # the current list.
        #
        copyable_lists = []
        for other_list in user.getShoppingLists():
            if other_list.id == shoppingList.id:
                continue
            if other_list.getItems().count() == 0:
                continue
            copyable_lists.append(other_list)
            
        #
        # Otherwise, set up the arguments for our template so
        # we can display the shoppingList contents.
        #
        return makeTemplateArgs(shopping_list=shoppingList,
                                shopping_list_items=shoppingList.getItems(),
                                user=user,
                                copyable_lists=copyable_lists,
                                )
    index.expose_resource = True
    
    
    
    @requiresLogin()
    @turbogears.expose()
    def new(self, name, user=None, **kwds):
        """Create a new shopping list.
        """
        name = name.strip()
        if not name:
            controllers.flash('Please enter a description of the item to add')
            raise cherrypy.HTTPRedirect('/list/lists')

        #
        # We don't know what database layer we're going
        # to use, so we don't know what exception we
        # get when we insert a duplicate.  So, we try
        # to do a lookup before the insert to detect
        # the existing item.
        #
        lists = ShoppingList.selectBy(user=user,
                                      name=name,
                                      )
        if lists.count() == 0:
            shopping_list = ShoppingList(user=user,
                                         name=name,
                                         )
            
        raise cherrypy.HTTPRedirect('/list/%s' % shopping_list.id)
    
    
    @requiresLogin()
    @turbogears.expose(html="grocerific.templates.shopping_lists")
    def lists(self, user=None, **kwds):
        """Show a user's shopping lists.
        """
        return makeTemplateArgs(shopping_lists=user.getShoppingLists())
    
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
        
        new_quantity = newQuantity
        new_quantity = new_quantity.replace('"', '')
        new_quantity = new_quantity.replace("'", '')
        
        to_update.quantity = new_quantity
        return makeTemplateArgs(shopping_list=shoppingList, 
                                shopping_list_items=shoppingList.getItems(),
                                )
    update.expose_resource = True


    
    @requiresLogin()
    @turbogears.expose(format="xml",
                       template="grocerific.templates.shopping_list_xml",
                       content_type="text/xml")
    def coupon(self, shoppingList, itemId=None, haveCoupon=None, user=None, **kwds):
        """Change the coupon status of an item in the list.
        """
        to_update = ShoppingListItem.get(itemId)
        if haveCoupon.lower() == 'yes':
            to_update.have_coupon = True
        elif haveCoupon.lower() == 'no':
            to_update.have_coupon = False
        else:
            raise ValueError('Do not know how to respond when haveCoupon="%s"' % haveCoupon)
        return makeTemplateArgs(shopping_list=shoppingList, 
                                shopping_list_items=shoppingList.getItems(),
                                )
    coupon.expose_resource = True


    
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

    
    @requiresLogin()
    @usesTransaction()
    @turbogears.expose()
    def clear(self, shoppingList, user=None, **kwds):
        """Clear the contents of a shopping list.
        """
        shoppingList.clearContents()
        raise cherrypy.HTTPRedirect('/list/%s' % shoppingList.id)
    clear.expose_resource = True

    
    @requiresLogin()
    @usesTransaction()
    @turbogears.expose()
    def delete(self, shoppingList, user=None, **kwds):
        """Clear the contents of a shopping list.
        """
        if shoppingList.name != NEXT_TRIP:
            shoppingList.destroySelf()
        else:
            controllers.flash('Cannot delete "Next Trip" lists')
        raise cherrypy.HTTPRedirect('/list/lists')
    delete.expose_resource = True
    
    
    @requiresLogin()
    @usesTransaction()
    @turbogears.expose()
    def import_list(self, shoppingList, copyFrom=None, user=None, **kwds):
        """Copy the contents of one shopping list to another.
        """
        source_list = ShoppingList.get(copyFrom)
        for item in source_list.getItems():
            shoppingList.add(item.item, item.quantity)
        raise cherrypy.HTTPRedirect('/list/%s/xml' % shoppingList.id)
    import_list.expose_resource = True
    
    
    @requiresLogin()
    @usesTransaction()
    @turbogears.expose()
    def duplicate(self, shoppingList, newName=None, user=None, **kwds):
        """Create a new shopping list and copy the contents
        of this list into it.
        """
        destination_list = ShoppingList(user=user,
                                        name=newName,
                                        )
        for item in shoppingList.getItems():
            destination_list.add(item.item, item.quantity)
        raise cherrypy.HTTPRedirect('/list/%s' % destination_list.id)
    duplicate.expose_resource = True

    
    
    @requiresLogin()
    @turbogears.expose(html="grocerific.templates.shopping_list_prep_print")
    def prepare_print(self, shoppingList=None, user=None, **kwds):
        return makeTemplateArgs(shopping_list=shoppingList,
                                stores=[ s.store for s in user.getStores() ],
                                user=user,
                                )
    prepare_print.expose_resource = True


    
    @requiresLogin()
    @turbogears.expose(html="grocerific.templates.shopping_list_print")
    def printable(self, shoppingList=None, user=None, **kwds):
        """Show the contents of a shopping list in a format convenient
        for printing.
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
            raise cherrypy.HTTPRedirect('/list/%s/prepare_print' % shoppingList.id)

        #
        # Figure out which stores to include
        #
        stores_to_include = []
        for kwd_name in kwds.keys():
            if kwd_name.startswith('store_'):
                try:
                    store_id = int(kwd_name[6:])
                except (TypeError, ValueError):
                    continue
                stores_to_include.append(store_id)

        if not stores_to_include:
            controllers.flash('Please select at least one store')
            raise cherrypy.HTTPRedirect('/list/%s/prepare_print' % shoppingList.id)
            

        #
        # All of the items in the list
        #
        all_items = shoppingList.getItems()

        #
        # Group items by store, then aisle.
        #
        items_without_aisles = []
        items_by_stores = {}
        for item_info in all_items:
            aisles = item_info.item.getAisles(user)
            found_aisle = False
            for aisle_info in aisles:
                if aisle_info.aisle:
                    items_by_aisle = items_by_stores.setdefault(aisle_info.store.id, {})
                    aisle_contents = items_by_aisle.setdefault(aisle_info.aisle, [])
                    aisle_contents.append(item_info)
                    found_aisle = True
            if not found_aisle:
                # This item didn't have any aisle info,
                # so put it in the "Unknown" store.
                items_without_aisles.append(item_info)

        #
        # Convert the items_by_stores data structure into
        # nested ordered lists that is easier to use in the
        # template.
        #
        grouped_items = []
        user_stores = [ (s.store.Name(), s.store.id)
                        for s in user.getStores()
                        if s.id in stores_to_include
                        ]
        user_stores.sort()
        for store_name, store_id in user_stores:
            items_by_aisles = items_by_stores.get(store_id, {}).items()
            if not items_by_aisles:
                continue
            sortable_items_by_aisles = []
            for aisle, items in items_by_aisles:
                try:
                    aisle_int = int(aisle)
                except (TypeError,ValueError):
                    aisle_int = None
                sortable_items_by_aisles.append((aisle_int, aisle, items))
            sortable_items_by_aisles.sort()
            items_by_aisles = [ (aisle, items)
                                for (aisle_int, aisle, items)
                                in sortable_items_by_aisles
                                ]
            grouped_items.append((store_name, items_by_aisles))

        #
        # Sort now so the template doesn't need to
        #
        items_without_aisles.sort()
                    
        return makeTemplateArgs(shopping_list=shoppingList,
                                items_without_aisles=items_without_aisles,
                                items_in_stores=grouped_items,
                                user=user,
                                stores=[ s[0] for s in user_stores ],
                                )
    printable.expose_resource = True
