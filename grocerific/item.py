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
    @usesTransaction()
    @usesLogin()
    def index(self, shoppingItem=None, user=None, **kwds):
        """Form to edit an item in the database.
        """
        if user:
            tags = user.getTagsForItem(shoppingItem)
            tag_names = [ tag.tag for tag in tags ]
            tag_names.sort()
            editable = True

            #
            # Determine which stores the user might go to when
            # shopping for this item.
            #
            active_store_ids = user.getStoreIdsForItem(shoppingItem)
        else:
            tag_names = []
            editable = False
            active_store_ids = []
        
        response = makeTemplateArgs(shopping_item=shoppingItem,
                                    user=user,
                                    tags=' '.join(tag_names),
                                    editable=editable,
                                    active_store_ids=active_store_ids,
                                    )
        return response
    index.expose_resource = True

    
    @turbogears.expose()
    @requiresLogin()
    @usesTransaction()
    def edit(self, shoppingItem=None, user=None, usuallyBuy=None, tags='', name=None, **args):
        """Change an item in the database.
        """
        #
        # The user might have changed the name of this thing
        #
        if name is not None:
            shoppingItem.name = name

        #
        # Change the per-user information
        #
        user_info = user.getItemInfo(shoppingItem)
        if usuallyBuy is not None:
            user_info.usuallybuy = usuallyBuy

        user.setTagsForItem(shoppingItem, tags)

        self._setAislesForItem(shoppingItem, user, **args)

        controllers.flash('Changes saved')
        
        raise cherrypy.HTTPRedirect('/item/%s' % shoppingItem.id)
    edit.expose_resource = True

    def _setAislesForItem(self, shoppingItem, user, **args):
        """Assign the aisle and store information for this item.
        """
        aisles_by_store = {}
        active_stores = []
        for key, value in args.items():

            if key.startswith('aisle_'):
                try:
                    store_id = int(key[6:])
                except ValueError:
                    continue
                aisles_by_store[store_id] = value
                
            elif key.startswith('store_'):
                try:
                    store_id = int(key[6:])
                except ValueError:
                    continue
                active_stores.append(store_id)

        shoppingItem.setAislesByStoreIds(aisles_by_store)
        user.setStoresForItem(shoppingItem, active_stores)
        return
    
    @turbogears.expose(html="grocerific.templates.item_new")
    @requiresLogin()
    def new_form(self, user=None, sourceId=None, name='', upc='', addToList=False, **args):
        """Form to add an item to the database.
        """
        if sourceId:
            source_obj = ShoppingItem.get(sourceId)
            name = source_obj.name
            tags = ' '.join([ t.tag for t in user.getTagsForItem(source_obj) ])
            aisles = source_obj.getAisles(user)
            active_store_ids = user.getStoreIdsForItem(source_obj)
        else:
            name = name or ''
            tags = ''
            aisles = []
            active_store_ids = []

        if upc and not name:
            try:
                info = ShoppingItem.getUPCInfo(upc)
                if info['found']:
                    name = info['description']
            except Exception, err:
                print 'Error with UPC lookup: %s' % str(err)
            
        return makeTemplateArgs(name=name,
                                upc=upc,
                                tags=tags,
                                aisles=aisles,
                                active_store_ids=active_store_ids,
                                user=user,
                                addToList=addToList,
                                )

    
    @turbogears.expose(format="xml",
                       template="grocerific.templates.query_results",
                       content_type="text/xml",
                       )
    @usesLogin()
    def search(self, queryString=None, user=None, **args):
        """Search for items in the database.
        """
        items = ShoppingItem.search(queryString, user)
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
                                query_string=queryString,
                                )

    
    @turbogears.expose(format="xml",
                       template="grocerific.templates.query_results",
                       content_type="text/xml",
                       )
    @usesLogin()
    def upcLookup(self, upc=None, user=None, **args):
        """Search for items in the database by UPC code.
        """
        items = ShoppingItem.upcLookup(upc, user)
        if items is not None:
            try:
                item_count = items.count()
            except (TypeError, AttributeError):
                item_count = len(items)
        else:
            items = []
            item_count = 0
        #
        # Format the response table
        #
        return makeTemplateArgs(shopping_items=items,
                                shopping_item_count=item_count,
                                upc=upc,
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

        #
        # Format the response table
        #
        return makeTemplateArgs(shopping_items=items,
                                shopping_item_count=item_count,
                                query_string=firstLetter,
                                )

    
    @turbogears.expose()
    @requiresLogin()
    @usesTransaction()
    def add(self, user=None, name='', tags='', upc='', addToList=False, shoppingListId=None, usuallyBuy=None, **args):
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
            item = ShoppingItem(name=name,
                                upc=upc,
                                )

        #
        # Update the usuallybuy info
        #
        if usuallyBuy:
            info = user.getItemInfo(item)
            info.usuallybuy = usuallyBuy

        user.setTagsForItem(item, tags)

        self._setAislesForItem(item, user, **args)

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

    @turbogears.expose(html="grocerific.templates.tags_list")
    @requiresLogin()
    def tags(self, user=None, **args):
        """Show the tags a user has used.
        """
        return makeTemplateArgs(tag_names=user.getTagNames(),
                                )
        
