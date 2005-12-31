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

    def getRememberMeCookieValue(self):
        """Returns a value to remember this user
        with moderate security.
        """
        m = md5.new()
        m.update('%s:%s' % (self.id, self.password))
        cookie_value = '%s %s' % (self.username, m.hexdigest())
        return cookie_value
    
class ShoppingItem(SQLObject):
    """Items someone can purchase.
    """
    name = StringCol(alternateID=True)

    
class ShoppingList(SQLObject):
    """Lists of things users have indicated that they want to buy.
    """
    name = StringCol()
    user = ForeignKey('User')

    def add(self, item):
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
            shopping_list_item = ShoppingListItem(list=self,
                                                  item=item,
                                                  quantity='1',
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

class ShoppingListItem(SQLObject):
    """Items someone has indicated that they may buy.
    """
    item = ForeignKey('ShoppingItem')
    list = ForeignKey('ShoppingList')
    quantity = StringCol()
    #have_coupon = BoolCol()
    
