<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - My Stores</title>
  </head>

  <body>
    <script>
      <!-- Search for stores in the database -->
      function findStores() {
        var queryString = document.findStore.query.value;
        if (queryString != "") {
          ajaxEngine.sendRequest('findStores', "queryString="+queryString);
        }
        return false;
      }

      <!-- Force an update of the current list -->
      function showList() {
        ajaxEngine.sendRequest('showList');
        return false;
      }

      <!-- Add the store with the given id to the list -->
      function addToList(storeId) {
        ajaxEngine.sendRequest('addToList', "storeId="+storeId);
        return false;
      }

      <!-- Remove the store with the given id from the list -->
      function removeFromList(userStoreId) {
        ajaxEngine.sendRequest('removeFromList', "userStoreId="+userStoreId);
        return false;
      }

      <!-- Pass the search parameters to the store add form. -->
      function goToNewStore() {
        var queryString = document.findStore.query.value;
        document.location.href = "/store/new_form?city=" + queryString;
      }

      function local_onload() {
        <!-- Set up query results -->
        ajaxEngine.registerRequest('findStores', '/store/search');
        ajaxEngine.registerAjaxElement('query_results');

        <!-- Set up current shopping list -->
        ajaxEngine.registerRequest('showList', '/store/xml');
        ajaxEngine.registerRequest('addToList', '/store/add');
        ajaxEngine.registerRequest('removeFromList', '/store/remove');
        ajaxEngine.registerAjaxElement('store_list');

        showList();
      }
      onloads.push(local_onload);

    </script>

    <h2>My Stores</h2>

    <fieldset>
      <legend>My Stores</legend>
      <div id="store_list">Loading...</div>
    </fieldset>

    <fieldset>
      <legend>Search by City</legend>

      <form name="findStore" onsubmit="return findStores()">
        <field>
          <input type="text" name="query" value="" />
          
          <input class="standalone" type="submit" name="search"
            value="Search" />
          
          <input class="standalone" type="submit" name="new"
            value="Tell us about a new store"
            onclick="return goToNewStore()"
            />
        </field>

      </form>
            
      <div class="query_results" id="query_results">
      </div>
    </fieldset>

  </body>
</html>