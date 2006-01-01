<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Welcome to Grocerific</title>
</head>

<body>
    <script>
      <!-- Search for items in the database -->
      function findItems() {
        var queryString = document.findItem.query.value;
        if (queryString != "") {
          ajaxEngine.sendRequest('findItems', "queryString="+queryString);
        }
        return false;
      }

      <!-- Add the item with the given id to the current list -->
      function addToList(itemId) {
        ajaxEngine.sendRequest('addToList', "itemId="+itemId.toString());
        return false;
      }

      <!-- Remove the item with the given id from the current list -->
      function removeFromList(itemId) {
        ajaxEngine.sendRequest('removeFromList', "itemId="+itemId);
        return false;
      }

      <!-- Force an update of the current list -->
      function showList() {
        ajaxEngine.sendRequest('showList');
        return false;
      }

      <!-- Pass the search parameters to the item add form. -->
      function goToNewItem() {
        var queryString = document.findItem.query.value;
        document.location.href = "/item/new_form?addToList=" + <span
        py:replace="shopping_list.id">list id</span> + unescape("&amp;") + "name=" + queryString;
      }

      <!-- Change the quantity of an item in the list -->
      function updateQuantity(shoppingListItemId, quantity) {
        var quantity_id = "quantity_" + shoppingListItemId;

        var new_quantity = prompt("Quantity", quantity);

        if (new_quantity != null) {
          ajaxEngine.sendRequest('updateQuantity',
                                 "itemId=" + shoppingListItemId,
                                  "newQuantity=" + new_quantity);
        }

        return false;
      }

      <!-- Import the contents of one list into this list. -->
      function importList() {
        var other_list_option_idx = document.import_form.copyFrom.selectedIndex;
        var other_list_option = document.import_form.copyFrom[other_list_option_idx];
        var other_list_id = other_list_option.value;

        ajaxEngine.sendRequest('importList', "copyFrom="+other_list_id);
        return false;
      }

      function onload() {
        <!-- Set up query results -->
        ajaxEngine.registerRequest('findItems', '/item/search');
        ajaxEngine.registerAjaxElement('query_results');

        <!-- Set up current shopping list -->
        ajaxEngine.registerRequest('showList', '/list/<span py:replace="shopping_list.id">list id</span>/xml');
        ajaxEngine.registerRequest('updateQuantity', '/list/<span py:replace="shopping_list.id">list id</span>/update');
        ajaxEngine.registerRequest('addToList', '/list/<span py:replace="shopping_list.id">list id</span>/add');
        ajaxEngine.registerRequest('removeFromList', '/list/<span py:replace="shopping_list.id">list id</span>/remove');
        ajaxEngine.registerRequest('importList', '/list/<span py:replace="shopping_list.id">list id</span>/import_list');
        ajaxEngine.registerAjaxElement('shopping_list');

        showList();
      }

    </script>

    <table>
      <tr valign="top">

        <td width="50%">
          <div class="shopping_list" id="shopping_list">
            <div class="list_name">Shopping List</div>
          </div>
        </td>

        <td>
          <div class="find_item">
            <h4>Find Item</h4>
            <form name="findItem" onsubmit="return findItems()">

              <div style="white-space: nowrap">
                <input type="text" name="query" value="" />
                
                <input class="standalone" type="submit" name="search"
                  value="Search" />
                
                <span><a onclick="goToNewItem()">Add a new item</a></span>
              </div>

              <div class="query_results" id="query_results">
                <table><tr><td></td></tr></table>
              </div>

            </form>
          </div>
        </td>

      </tr>
    </table>

    <form py:attrs="{'action':'/list/%s/clear' % shopping_list.id}" method="post">
      <input class="standalone" type="submit" name="clearBtn"
        value="Clear this list" />
    </form>

    <form py:attrs="{'action':'/list/%s/delete' % shopping_list.id}" 
      method="post"
      py:if="not shopping_list.name == 'Next Trip'">
      <input class="standalone" type="submit" name="deleteBtn"
        value="Delete this list" />
    </form>

    <form name="import_form" onsubmit="return importList()">
      <input class="standalone" type="submit" name="copyBtn"
        value="Copy contents from" />

      <select size="1" id="copyFrom" name="copyFrom">
        <option py:for="other_list in user.getShoppingLists()"
          py:if="(other_list.getItems().count() > 0) and
          (other_list.id != shopping_list.id)"
          py:attrs="{'value':other_list.id}" 
          py:content="other_list.name">Name</option>
      </select>

    </form>
    
</body>
</html>