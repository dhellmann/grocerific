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


def cleanString(s):
    """Clean up a string to make it safe to pass to SQLObject
    as a query.
    """
    for bad, good in [ ("'", ''),
                       ('"', ''),
                       (';', ''),
                       ]:
        s = s.replace(bad, good)
    return s


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
        aisle = cleanString(aisle)
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

    def search(cls, queryString):
        """Run a text search for the query string.
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
            where_clauses.append(ShoppingItem.q.name.contains(word))

        #
        # Assemble the select string and get the items.
        #
        if where_clauses:
            if len(where_clauses) == 0:
                raise ValueError('Invalid query string')
            elif len(where_clauses) == 1:
                select_expr = where_clauses[0]
            else:
                where_clauses = tuple(where_clauses)
                select_expr = AND(*where_clauses)
            items = ShoppingItem.select(select_expr,
                                        orderBy='name',
                                        )
        else:
            items = None
        return items
    search = classmethod(search)

    def browse(cls, firstLetter):
        """Produce a list of ShoppingItems that start with firstLetter.
        """
        where_clauses = []
        clean_first_letter = cleanString(firstLetter)
        if clean_first_letter == '#':
            for i in range(0, 10):
                where_clauses.append(ShoppingItem.q.name.startswith(str(i)))
        elif clean_first_letter:
            where_clauses.append(ShoppingItem.q.name.startswith(clean_first_letter))

        if where_clauses:
            if len(where_clauses) == 0:
                raise ValueError('Invalid query string')
            elif len(where_clauses) == 1:
                select_expr = where_clauses[0]
            else:
                where_clauses = tuple(where_clauses)
                select_expr = OR(*where_clauses)

            items = ShoppingItem.select(select_expr,
                                        orderBy='name',
                                        )
        else:
            items = None
        return items
    browse = classmethod(browse)
    

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

    def add(self, item, quantity=None, haveCoupon=False):
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
                                                  have_coupon=haveCoupon,
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
    have_coupon = BoolCol()

    
class Store(SQLObject):
    """A place where a user can shop.
    """
    chain = StringCol()
    city = StringCol()
    location = StringCol()

    def search(cls, city):
        """Search for stores in a city.
        """
        #
        # Clean up the string we are given and turn it
        # into words that might appear in the name
        # of a shopping item.
        #
        clean_query_string = cleanString(city)
        if clean_query_string:
            select_expr = Store.q.city.contains(clean_query_string)
            stores = Store.select(select_expr,
                                  orderBy=(Store.q.chain,
                                           Store.q.city,
                                           Store.q.location,
                                           ))
        else:
            stores = None
        return stores
    search = classmethod(search)

    
    
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
    
