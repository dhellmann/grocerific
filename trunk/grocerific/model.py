#
# $Id$
#
# Copyright (c) 2005 Racemi, Inc.  All rights reserved.
#

"""Database model.

"""

#
# Import system modules
#
import md5
from sqlobject import *
from turbogears.database import PackageHub

#
# Import Local modules
#


#
# Module
#

hub = PackageHub("grocerific")
__connection__ = hub


class User(SQLObject):
    """Users of the site.
    """
    class sqlmeta:
        # 'user' is a reserved word in some databases,
        # so give a different name for the table.
        table = 'siteuser'
    username = StringCol(alternateID=True)
    password = StringCol(notNull=True)
    email = StringCol()
    lists = MultipleJoin('ShoppingList')
    location = StringCol()

    def getRememberMeCookieValue(self):
        """Returns a value to remember this user
        with moderate security.
        """
        m = md5.new()
        m.update('%s:%s' % (self.id, self.password))
        cookie_value = '%s %s' % (self.username, m.hexdigest())
        return cookie_value

    def getShoppingLists(self):
        """Return the ShoppingLists owned by this user.
        """
        return ShoppingList.selectBy(user=self,
                                     orderBy='name',
                                     )

    def getStores(self):
        """Return the stores frequented by the user.
        """
        return UserStore.select(
            """
            user_store.user_id = %s
            AND
            user_store.store_id = store.id
            
            ORDER BY
              store.chain,
              store.city,
              store.location
            """ % self.id,
            clauseTables=['store'],
            )

    def addStore(self, store):
        """Add a store to the list of stores this user frequents.
        """
        # See if there is already a relationship
        # with that store before adding a new one.
        existing = UserStore.selectBy(user=self,
                                      store=store,
                                      )
        if existing.count() == 0:
            user_store = UserStore(user=self, store=store)
        return

    
    
class ShoppingItem(SQLObject):
    """Items someone can purchase.
    """
    name = StringCol(alternateID=True)

    def getUserInfo(self, user):
        """Returns a ShoppingItemInfo for the user and this item.
        """
        info_list = ShoppingItemInfo.selectBy(user=user,
                                              item=self,
                                              )
        try:
            return info_list[0]
        except IndexError:
            return ShoppingItemInfo(user=user, item=self)

    def setAisle(self, store, aisle):
        """Set which aisle an item is in for a store.
        """
        existing_aisle_info = AisleItem.selectBy(store=store,
                                                 item=self,
                                                 )
        if existing_aisle_info.count() != 0:
            aisle_info = existing_aisle_info[0]
            aisle_info.aisle = aisle
        else:
            aisle_info = AisleItem(store=store, item=self, aisle=aisle)
        return aisle_info

    def getAisles(self, user):
        """Returns a sequence of AisleItem instances
        for the stores which are members of the user's
        "My Stores" list.
        """
        response = []
        stores = user.getStores()
        for store in stores:
            existing_aisle_info = AisleItem.selectBy(store=store,
                                                     item=self,
                                                     )
            if existing_aisle_info.count() != 0:
                aisle_info = existing_aisle_info[0]
            else:
                aisle_info = self.setAisle(store, None)
            response.append(aisle_info)
        return response

class ShoppingItemInfo(SQLObject):
    """User-specific information about a shopping item.
    """
    user = ForeignKey('User')
    item = ForeignKey('ShoppingItem')
    usuallybuy = StringCol(default='1')

    
class ShoppingList(SQLObject):
    """Lists of things users have indicated that they want to buy.
    """
    name = StringCol()
    user = ForeignKey('User')

    def add(self, item, quantity=None):
        """Add an item to a shopping list, if it does
        not already exist in the list.
        """
        #
        # Make sure the item isn't already in the list
        # before adding it.
        #
        existing_items = ShoppingListItem.selectBy(list=self,
                                                   item=item,
                                                   )
        if existing_items.count() == 0:
            if quantity is None:
                user_info = item.getUserInfo(self.user)
                quantity = user_info.usuallybuy
            shopping_list_item = ShoppingListItem(list=self,
                                                  item=item,
                                                  quantity=quantity,
                                                  )
        return
            
    def getItems(self):
        return ShoppingListItem.select(
            """
            shopping_list_item.list_id = %s
            AND
            shopping_list_item.item_id = shopping_item.id
            ORDER BY shopping_item.name
            """ % self.id,
            clauseTables=['shopping_item'],
            )

    def clearContents(self):
        """Clear all of the items from the list.
        """
        items = self.getItems()
        for item in items:
            item.destroySelf()
        return

    def destroySelf(self):
        self.clearContents()
        SQLObject.destroySelf(self)
        return

    
class ShoppingListItem(SQLObject):
    """Items someone has indicated that they may buy.
    """
    item = ForeignKey('ShoppingItem')
    list = ForeignKey('ShoppingList')
    quantity = StringCol()
    #have_coupon = BoolCol()

    
class Store(SQLObject):
    """A place where a user can shop.
    """
    chain = StringCol()
    city = StringCol()
    location = StringCol()

    
class UserStore(SQLObject):
    """A store where a user regularly shops.
    """
    user = ForeignKey('User')
    store = ForeignKey('Store')

        
class AisleItem(SQLObject):
    """Which aisle an item appears in.
    """
    item = ForeignKey('Item')
    store = ForeignKey('Store')
    aisle = StringCol()
    
