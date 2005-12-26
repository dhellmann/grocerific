from sqlobject import *
from turbogears.database import PackageHub

hub = PackageHub("grocerific")
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass
