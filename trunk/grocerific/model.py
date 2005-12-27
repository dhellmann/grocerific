from sqlobject import *
from turbogears.database import PackageHub

hub = PackageHub("grocerific")
__connection__ = hub

class User(SQLObject):
    class sqlmeta:
        # 'user' is a reserved word in some databases,
        # so give a different name for the table.
        table = 'siteuser'
    username = StringCol(alternateID=True)
    password = StringCol(notNull=True)
    email = StringCol()
    lists = MultipleJoin('ShoppingList')

class ShoppingItem(SQLObject):
    name = StringCol(alternateID=True)

class ShoppingList(SQLObject):
    name = StringCol()
    user = ForeignKey('User')

    def getItems(self):
        return ShoppingListItem.selectBy(list=self,
                                         orderBy='item.name')

class ShoppingListItem(SQLObject):
    item = ForeignKey('ShoppingItem')
    list = ForeignKey('ShoppingList')
    quantity = StringCol()

