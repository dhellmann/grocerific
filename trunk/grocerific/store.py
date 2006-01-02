#
# $Id: init.el,v 1.6 2005/07/11 14:27:19 dhellmann Exp $
#
# Copyright (c) 2005 Racemi, Inc.  All rights reserved.
#

"""Store controller

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

class StoreController(RESTResource):
    """Controller for store-related functions.
    """

    def REST_instantiate(self, storeId, **kwds):
        """Look for the store by it's primary id.
        """
        try:
            return Store.get(storeId)
        except SQLObjectNotFound:
            return None

    def REST_create(self, *args, **kwds):
        """Create a new list?
        FIXME - Not sure when this is called.
        """
        raise NotImplementedError()


    
    @requiresLogin()
    @turbogears.expose(html="grocerific.templates.store_edit")
    def index(self, store=None, user=None, **kwds):
        """Show information about a store.
        """
        return makeTemplateArgs(user=user,
                                store=store,
                                )
    index.expose_resource = True


    @usesTransaction()
    @requiresLogin()
    @turbogears.expose()
    def edit(self, store, user=None, chain=None, city=None, location=None, **kwds):
        """Change information about a store.
        """
        if chain is not None:
            store.chain = chain
        if city is not None:
            store.city = city
        if location is not None:
            store.location = location
        raise cherrypy.HTTPRedirect('/store/%s' % store.id)
    edit.expose_resource = True

    
    
    @requiresLogin()
    @turbogears.expose(html="grocerific.templates.store_list")
    def my(self, user=None, **kwds):
        """Show all of a user's stores.
        """
        stores = user.getStores()
        return makeTemplateArgs(user=user,
                                stores=stores,
                                )

    

    @requiresLogin()
    @turbogears.expose(format="xml",
                       template="grocerific.templates.store_list_xml",
                       content_type="text/xml")
    def xml(self, user=None, **kwds):
        """Returns an AJAX-ready XML version of the list of stores.
        """
        stores = user.getStores()
        return makeTemplateArgs(user=user,
                                stores=stores,
                                )


    
    @turbogears.expose(format="xml",
                       template="grocerific.templates.store_query_results",
                       content_type="text/xml",
                       )
    @usesLogin()
    def search(self, queryString=None, **args):
        """Search for stores in the database.
        """
        #
        # Clean up the string we are given and turn it
        # into words that might appear in the name
        # of a shopping item.
        #
        clean_query_string = cleanString(queryString)
        if clean_query_string:
            select_string = """
            store.city LIKE '%%%s%%'

            ORDER BY
              store.chain,
              store.city,
              store.location
            """ % clean_query_string
            stores = Store.select(select_string)
            store_count = stores.count()
        else:
            stores = []
            store_count = 0

        #
        # Format the response table
        #
        response= makeTemplateArgs(stores=stores,
                                   store_count=store_count,
                                   )
        return response


    
    @requiresLogin()
    @turbogears.expose(format="xml",
                       content_type="text/xml")
    def remove(self, userStoreId, itemId=None, user=None, **kwds):
        """Remove the UserStore.
        """
        try:
            existing_item = UserStore.get(userStoreId)
        except SQLObjectNotFound:
            controllers.flash('Unrecognized store')
            response = '<ajax-response/>'
        else:
            existing_item.destroySelf()
            raise cherrypy.HTTPRedirect('/store/xml')

        return response


    
    @requiresLogin()
    @turbogears.expose(format="xml",
                       content_type="text/xml")
    def add(self, storeId, user=None, **kwds):
        """Add a store to my list.
        """
        try:
            store = Store.get(storeId)
        except SQLObjectNotFound:
            controllers.flash('Unrecognized store')
            raise cherrypy.HTTPRedirect('/store/my')
        else:
            user.addStore(store)
            raise cherrypy.HTTPRedirect('/store/xml')

        
    @turbogears.expose(html="grocerific.templates.store_new")
    @requiresLogin()
    def new_form(self, user=None, name='', addToList=False, city=None, **args):
        """Form to add a store to the database.
        """
        return makeTemplateArgs(name=name,
                                addToList=addToList,
                                city=city or user.location,
                                )

    
    @turbogears.expose()
    @requiresLogin()
    @usesTransaction()
    def new(self, user=None, chain=None, city=None, location=None, addToList=False, **args):
        """Form to add a store to the database.
        """
        existing = Store.selectBy(chain=chain,
                                  city=city,
                                  location=location,
                                  )
        if existing.count() == 0:
            new_store = Store(chain=chain,
                              city=city,
                              location=location,
                              )
        else:
            new_store = existing[0]
            
        if addToList:
            user.addStore(new_store)
        raise cherrypy.HTTPRedirect('/store/%s' % new_store.id)