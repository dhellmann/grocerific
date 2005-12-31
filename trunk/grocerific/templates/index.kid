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
        ajaxEngine.sendRequest('removeFromList', "itemId="+itemId.toString());
        return false;
      }

      <!-- Force an update of the current list -->
      function showList() {
        ajaxEngine.sendRequest('showList', "listName='Next Trip'");
        return false;
      }

      <!-- Pass the search parameters to the item add form. -->
      function goToAddItem() {
        var queryString = document.findItem.query.value;
        document.location.href = "/item/add_form?addToList=1" + unescape("&amp;") + "name=" + queryString;
      }

      <!-- Show a text field to let the user edit the quantity of an -->
      function updateQuantity(shoppingListItemId, quantity) {
        var quantity_id = "quantity_" + shoppingListItemId;

        var new_quantity = prompt("Quantity", quantity);

        if (new_quantity != null) {
          ajaxEngine.sendRequest('showList', 
                                 "itemId=" + shoppingListItemId,
                                 "listName='Next Trip'",
                                  "newQuantity=" + new_quantity);
        }

        return false;
      }

      function onload() {
        <!-- Set up query results -->
        ajaxEngine.registerRequest('findItems', '/item/findItems');
        ajaxEngine.registerAjaxElement('query_results');

        <!-- Set up current shopping list -->
        ajaxEngine.registerRequest('showList', '/item/showList');
        ajaxEngine.registerRequest('addToList', '/item/addToList');
        ajaxEngine.registerRequest('removeFromList', '/item/removeFromList');
        ajaxEngine.registerAjaxElement('shopping_list');

        showList();
      }

    </script>

    <table py:if="not session_is_logged_in">
      <tr valign="top">
        
        <td width="20%">
          <div py:replace="loginBox()"/>
        </td>

        <td>
          <div py:if="not session_is_logged_in">
            Site welcome message and description goes here.
          </div>
        </td>
      </tr>
    </table>

    <table py:if="session_is_logged_in">
      <tr valign="top">

        <td width="50%">
          <div class="shopping_list" id="shopping_list" py:if="session_is_logged_in">
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
                
                <span><a onclick="goToAddItem()">Add a new item</a></span>
              </div>

              <div class="query_results" id="query_results">
                <table><tr><td></td></tr></table>
              </div>

            </form>
          </div>

        </td>
      </tr>
    </table>
    
</body>
</html>