from sqlobject import *
from turbogears.database import PackageHub

hub = PackageHub("grocerific")
__connection__ = hub

class User(SQLObject):
    username = StringCol(alternateID=True)
    password = StringCol(notNull=True)
    email = StringCol()

# class YourDataClass(SQLObject):
#     pass
