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
from sqlobject.sqlbuilder import *
from turbogears.database import PackageHub

#
# Import Local modules
#


#
# Module
#

hub = PackageHub("grocerific")
__connection__ = hub

#
# Force table creation order
#
soClasses = ( 'User', 
              'ShoppingItem', 
              'ShoppingItemInfo', 
              'ShoppingItemTag', 
              'ShoppingList', 
              'ShoppingListItem', 
              'Store', 
              'UserStore', 
              'AisleItem',
              'StoreItem',
              )

    
def cleanString(s):
    """Clean up a string to make it safe to pass to SQLObject
    as a query.
    """
    if s is None:
        return ''
    for bad, good in [ ("'", ''),
                       ('"', ''),
                       (';', ''),
                       ('%', '%%'),
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

    def getStores(self, ordered=True):
        """Return the stores frequented by the user.
        """
        if ordered:
            orderby = """
            ORDER BY
              store.chain,
              store.city,
              store.location
            """
        else:
            orderby = ''
            
        return UserStore.select(
            """
            user_store.user_id = %s
            AND
            user_store.store_id = store.id

            %s
            """ % (self.id, orderby),
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

    def getTagNames(self):
        """Return unique tag names used by this user.
        """
        rows = hub.hub.getConnection().queryAll("""
        SELECT
            DISTINCT(tag)
        FROM
            shopping_item_tag
        WHERE
            user_id = %d
        ORDER BY
            tag
        """ % self.id)
        return [ r[0]
                 for r in rows
                 ]

    def getTagsForItem(self, item):
        """Returns the tags the user has specified for the item.
        """
        if not item:
            return []
        all_tags = ShoppingItemTag.selectBy(user=self,
                                            item=item,
                                            )
        return all_tags

    def setTagsForItem(self, item, tagsString):
        """Set the names of the tags the user has specified
        for the item.
        """
        if not item:
            return

        #
        # Figure out what we already know about the item
        #
        existing_tags = ShoppingItemTag.selectBy(user=self, item=item)
        existing_tags_map = {}
        for t in existing_tags:
            existing_tags_map[t.tag] = t
        existing_tag_names = existing_tags_map.keys()

        #
        # Add new tags
        #
        tags = cleanString(tagsString).split(' ')
        for tag_name in tags:
            tag_name = tag_name.strip()
            if not tag_name:
                continue
            if tag_name in existing_tag_names:
                # Already had this one and want to
                # keep it.  Drop it from the map
                # so we don't delete it below.
                try:
                    del existing_tags_map[tag_name]
                except KeyError:
                    pass
            else:
                new_tag = ShoppingItemTag(user=self, item=item, tag=tag_name)
                existing_tag_names.append(tag_name)

        #
        # Remove tags we weren't given
        #
        for tag_name, tag_obj in existing_tags_map.items():
            tag_obj.destroySelf()
        return

    def getItemInfo(self, item):
        """Returns a ShoppingItemInfo for the user and this item.
        """
        info_list = ShoppingItemInfo.selectBy(user=self,
                                              item=item,
                                              )
        try:
            return info_list[0]
        except IndexError:
            return ShoppingItemInfo(user=self, item=item)
        

    def getStoreInfoForItem(self, store, item):
        """Returns the StoreItem for the item and
        this user.
        """
        existing_store_info = StoreItem.selectBy(store=store,
                                                 item=item,
                                                 user=self,
                                                 )
        if existing_store_info.count() != 0:
            store_info = existing_store_info[0]
        else:
            store_info = StoreItem(store=store, item=item, user=self)
        return store_info

    def getStoreIdsForItem(self, item):
        """Returns a list of stores the user might go to
        when shopping for the item.
        """
        store_items = StoreItem.selectBy(item=item,
                                         user=self,
                                         #buy_here=True,
                                         )
        store_ids = [ store_item.store.id
                      for store_item in store_items
                      if store_item.buy_here
                      ]
        if (not store_ids) and (not store_items.count()):
            #
            # Assume they might buy in any store
            #
            store_ids = [ store_info.store.id
                          for store_info in self.getStores()
                          ]
        return store_ids

    def setStoresForItem(self, item, storeIds):
        """Given a list of store ids, mark those stores
        as being places the user will buy the item.
        Mark the other stores in the user's My Stores
        list as places the user will not buy the item.
        """
        for user_store in self.getStores():

            store = user_store.store

            store_info = self.getStoreInfoForItem(store, item)
            
            #
            # A place they will buy the item
            #
            if ( (store.id in storeIds)
                 and
                 (not store_info.buy_here)
                 ):
                store_info.buy_here = True
                
            #
            # A place they will not buy the item
            #
            if ( (store_info.store.id not in storeIds)
                 and
                 (store_info.buy_here)
                 ):
                store_info.buy_here = False

        return
    
class ShoppingItem(SQLObject):
    """Items someone can purchase.
    """
    name = StringCol(alternateID=True)

##    def _create(self, id, **kw):
##        m = md5.new()
##        m.update(str(id))
##        self.hash = m.hexdigest()[:10]
##        print 'NEW %s: %s => %s' % (self.__class__.__name__, id, self.hash)
##        return SQLObject._create(self, id, **kw)

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def setAislesByStoreIds(self, aislesByStore):
        """Given a mapping of store id to aisle string,
        update the database.
        """
        for store_id, aisle in aislesByStore.items():
            store = Store.get(store_id)
            self.setAisle(store, aisle)
        return

    def setAisle(self, store, aisle):
        """Set which aisle an item is in for a store.
        """
        aisle = cleanString(aisle)
        existing_aisle_info = AisleItem.selectBy(store=store,
                                                 item=self,
                                                 )
        if existing_aisle_info.count() != 0:
            try:
                aisle_info = existing_aisle_info[0]
            except IndexError:
                aisle_info = AisleItem(store=store,
                                       item=self,
                                       aisle=aisle,
                                       )
            else:
                if aisle_info.aisle != aisle:
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
        user_stores = user.getStores()
        for user_store in user_stores:
            store = user_store.store
            existing_aisle_info = AisleItem.selectBy(store=store,
                                                     item=self,
                                                     )
            if existing_aisle_info.count() != 0:
                aisle_info = existing_aisle_info[0]
            else:
                aisle_info = self.setAisle(store, None)
            response.append(aisle_info)
        return response

    def search(cls, queryString, user=None):
        """Run a text search for the query string.
        """
        #
        # Clean up the string we are given and turn it
        # into words that might appear in the name
        # of a shopping item.
        #
        clean_query_string = cleanString(queryString)
        words = clean_query_string.split(' ')
        name_clauses = []
        tag_clauses = []
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

            #
            # Use case-insensitive comparison
            #
            name_clauses.append(
                SQLConstant("LOWER(shopping_item.name) LIKE '%%%s%%'" % \
                            word.lower())
                )

            #
            # Look for the word as a tag
            #
            if user:
                tag_clauses.append(
                    IN(word.lower(),
                       Select(SQLConstant("LOWER(shopping_item_tag.tag)"),
                              where=AND(ShoppingItemTag.q.userID == user.id,
                                        #
                                        # If we use the normal comparison,
                                        # the subquery reference will be to
                                        # a separate table reference in the
                                        # subquery so we use a constant
                                        # expression here.
                                        #
                                        SQLConstant('item_id = shopping_item.id'),
                                        )
                              )
                       )
                    )
                
        #
        # Assemble the select string and get the items.
        #
        name_select = None
        tag_select = None
        
        if len(name_clauses) == 1:
            name_select = name_clauses[0]
        elif name_clauses:
            name_clauses = tuple(name_clauses)
            name_select = AND(*name_clauses)

        if len(tag_clauses) == 1:
            tag_select = tag_clauses[0]
        elif tag_clauses:
            tag_clauses = tuple(tag_clauses)
            tag_select = AND(*tag_clauses)

        if name_select and tag_select:
            select_expr = OR(name_select, tag_select)
        elif name_select:
            select_expr = name_select
        elif tag_select:
            select_expr = tag_select
        else:
            return None
        
        items = ShoppingItem.select(select_expr,
                                    orderBy='name',
                                    )
        #print items
        return items
    search = classmethod(search)

    def browse(cls, firstLetter):
        """Produce a list of ShoppingItems that start with firstLetter.
        """
        where_clauses = []
        clean_first_letter = cleanString(firstLetter)
        if clean_first_letter == '#':
            for i in range(0, 10):
                where_clauses.append(OR(ShoppingItem.q.name.startswith(str(i).lower()),
                                        ShoppingItem.q.name.startswith(str(i).upper()),
                                        ))
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

    def getTagNames(self):
        """Returns the tags any user has specified for the item.
        """
        names = []
        for tag in ShoppingItemTag.selectBy(item=self):
            if tag.tag not in names:
                names.append(tag.tag)
        names.sort()
        return names

    def getForeignTagNames(self, user):
        """Returns the tags any user other than the named
        user has specified for the item.
        """
        names = []
        for tag in ShoppingItemTag.selectBy(item=self):
            if tag.user == user:
                continue
            if tag.tag not in names:
                names.append(tag.tag)
        names.sort()
        return names
    

class ShoppingItemInfo(SQLObject):
    """User-specific information about a shopping item.
    """
    user = ForeignKey('User')
    item = ForeignKey('ShoppingItem')
    usuallybuy = StringCol(default='1')

class ShoppingItemTag(SQLObject):
    """User-specific classification tag for a shopping item.
    """
    user = ForeignKey('User')
    item = ForeignKey('ShoppingItem')
    tag = StringCol(notNull=True)

    
class ShoppingList(SQLObject):
    """Lists of things users have indicated that they want to buy.
    """
    name = StringCol(notNull=True)
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
                user_info = self.user.getItemInfo(item)
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
            ORDER BY LOWER(shopping_item.name)
            """ % self.id,
            clauseTables=['shopping_item'],
            )

    def getItemCount(self):
        return ShoppingListItem.selectBy(list=self).count()

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

    def _getItemsWithAisles(self, storeIdsToInclude):
        """Return a sequence of nested lists organized by:

        [ (store, [(aisle, [items])]) ]
        """
        if len(storeIdsToInclude) < 1:
            raise ValueError('Please specify at least one store')
        elif len(storeIdsToInclude) == 1:
            store_ids = storeIdsToInclude[0]
            store_id_test = '='
        else:
            store_ids = str(tuple(storeIdsToInclude))
            store_id_test = 'IN'
            
        sql = """
        SELECT
	      CASE store.location
            WHEN '' THEN store.chain
            WHEN NULL THEN store.chain
            ELSE store.chain || ' @ ' || store.location 
          END as store_fullname,
          aisle_item.aisle,
          shopping_item.id,
          shopping_item.name,
          shopping_list_item.quantity,
          shopping_list_item.have_coupon
          
        FROM
          siteuser,
          store,
          user_store,
          shopping_list_item,
          shopping_item,
          aisle_item LEFT OUTER JOIN
            (select * from store_item where user_id = %(user_id)s and buy_here) store_item
            ON aisle_item.item_id = store_item.item_id
          
        WHERE

          -- limits based on parameters
          shopping_list_item.list_id = %(shopping_list_id)s
          AND
          siteuser.id = %(user_id)s
          AND
          store.id %(store_id_test)s %(store_ids)s

          AND

          -- items in the list
          shopping_item.id = shopping_list_item.item_id

          AND

          -- stores frequented by the user
          user_store.user_id = siteuser.id
          AND
          user_store.store_id = store.id

          AND
          
          -- stores where the user buys this item
          (store_item.id is null
           OR
           (store_item.item_id = shopping_item.id
            AND
            store_item.store_id = store.id
           )
          )
          
          AND

          -- stores where there is a known aisle for this item
          aisle_item.item_id = shopping_item.id
          AND
          aisle_item.store_id = store.id
          AND
          aisle_item.aisle is not null
          AND
          aisle_item.aisle <> ''

        ORDER BY
          store_fullname,
          aisle_item.aisle,
          shopping_item.name
        """ % { 'user_id':self.user.id,
                'shopping_list_id':self.id,
                'store_ids':store_ids,
                'store_id_test':store_id_test,
                }
        conn = hub.getConnection()
        results = conn.queryAll(sql)

        #
        # Organize the results
        #
        items_by_stores = {}
        for row in results:
            store = row[0]
            items_by_aisles = items_by_stores.setdefault(store, {})

            aisle = row[1]
            items = items_by_aisles.setdefault(aisle, [])

            items.append(PrintableItem(*tuple(row[2:])))

        #
        # Convert to nested lists
        # and resort the aisles 
        # to get the numbered aisles
        # in the right order.
        #
        items_with_aisles = []
        for store, items_by_aisles in items_by_stores.items():
            sortable_items_by_aisles = []
            for aisle, items in items_by_aisles.items():
                try:
                    sortable_aisle = int(aisle)
                except ValueError:
                    sortable_aisle = aisle
                #
                # Sort in the aisle
                #
                items.sort()
                
                sortable_items_by_aisles.append((sortable_aisle, items))

            #
            # Sort the aisles
            #
            sortable_items_by_aisles.sort()
            items_by_aisles = [ (str(aisle), items)
                                for aisle, items in sortable_items_by_aisles
                                ]
            items_with_aisles.append((store, items_by_aisles))

        #
        # Sort by store
        #
        items_with_aisles.sort()

        return items_with_aisles

    def _getItemsWithoutAisles(self, storeIdsToInclude):
        """Produce a mapping of the items that do not have
        aisle information, keyed by the name of the store
        where the user expects to buy those items.
        """
        if len(storeIdsToInclude) < 1:
            raise ValueError('Please specify at least one store')
        elif len(storeIdsToInclude) == 1:
            store_ids = storeIdsToInclude[0]
            store_id_test = '='
        else:
            store_ids = str(tuple(storeIdsToInclude))
            store_id_test = 'IN'
            
        sql = """
        SELECT
	      CASE store.location
            WHEN '' THEN store.chain
            WHEN NULL THEN store.chain
            ELSE store.chain || ' @ ' || store.location 
          END as store_fullname,
          shopping_item.id,
          shopping_item.name,
          shopping_list_item.quantity,
          shopping_list_item.have_coupon
          
        FROM
          siteuser,
          store,
          user_store,
          shopping_list_item,
          shopping_item LEFT OUTER JOIN
            (select * from store_item where user_id = %(user_id)s
              and store_id %(store_id_test)s %(store_ids)s
			 and buy_here) store_item
            ON shopping_item.id = store_item.item_id
          
        WHERE

          -- limits based on parameters
          shopping_list_item.list_id = %(shopping_list_id)s
          AND
          siteuser.id = %(user_id)s

          AND

          -- items in the list
          shopping_item.id = shopping_list_item.item_id

          AND

          -- stores used by the shopper for this trip
          user_store.user_id = siteuser.id
          AND
          user_store.store_id = store.id
		  AND
		  user_store.store_id %(store_id_test)s %(store_ids)s

          AND
          
          -- stores where the user buys this item
          (store_item.id is null
           OR
           (store_item.item_id = shopping_item.id
            AND
            store_item.store_id = store.id
           )
          )

          AND

          -- No aisle
          shopping_item.id not in
            (SELECT
               aisle_item.item_id
               
             FROM
               aisle_item LEFT OUTER JOIN
                (select * from store_item where user_id = %(user_id)s
				 and buy_here) store_item
                ON aisle_item.item_id = store_item.item_id
                
             WHERE
               aisle_item.store_id %(store_id_test)s %(store_ids)s
               AND
               aisle_item.aisle is not null
               AND
               aisle_item.aisle <> ''
               )

        ORDER BY

          store_fullname,
		  shopping_item.name
        """ % { 'user_id':self.user.id,
                'shopping_list_id':self.id,
                'store_ids':store_ids,
                'store_id_test':store_id_test,
                }
        conn = hub.getConnection()
        results = conn.queryAll(sql)

        #
        # Organize the results by store
        #
        items_without_aisles = {}
        for row in results:
            store_name = row[0]
            item = PrintableItem(*tuple(row[1:]))
            items = items_without_aisles.setdefault(store_name, [])
            items.append(item)

        return items_without_aisles

    def getPrintableItems(self, storeIdsToInclude):
        items_with_aisles = self._getItemsWithAisles(storeIdsToInclude)
        items_without_aisles = self._getItemsWithoutAisles(storeIdsToInclude)

        #
        # Merge the 2 sets of data
        #
        items = []
        for store_name, items_by_aisle in items_with_aisles:
            store_no_aisle = items_without_aisles.get(store_name)
            if store_no_aisle:
                items_by_aisle.insert(0, ('Unknown', store_no_aisle))
            items.append( (store_name, items_by_aisle) )
        
        return items

class PrintableItem:
    """Just used for returning printable list.
    """
    def __init__(self, id, name, quantity, haveCoupon):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.have_coupon = haveCoupon
        return

    def __cmp__(self, other):
        return cmp(self.name, other.name)
    
class ShoppingListItem(SQLObject):
    """Items someone has indicated that they may buy.
    """
    item = ForeignKey('ShoppingItem')
    list = ForeignKey('ShoppingList')
    quantity = StringCol()
    have_coupon = BoolCol(default=False)

    def __cmp__(self, other):
        return cmp(self.item, other.item)

    
class Store(SQLObject):
    """A place where a user can shop.
    """
    chain = StringCol()
    city = StringCol()
    location = StringCol()

    def Name(self):
        """Return a nicely formatted name for the store.
        """
        if self.location:
            return '%s @ %s' % (self.chain, self.location)
        return self.chain

    _get_name = Name

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
            select_expr = SQLConstant("LOWER(store.city) LIKE '%%%s%%'" % \
                                      clean_query_string)
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
    """Which aisle an item appears in for a given store.
    """
    item = ForeignKey('ShoppingItem')
    store = ForeignKey('Store')
    aisle = StringCol()
    
        
class StoreItem(SQLObject):
    """Which stores a user might shop in for an item.
    """
    item = ForeignKey('ShoppingItem')
    store = ForeignKey('Store')
    user = ForeignKey('User')
    buy_here = BoolCol(default=True)
    
