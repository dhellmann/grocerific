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

      function onload() {
        ajaxEngine.registerRequest('findItems', '/item/findItems');
        ajaxEngine.registerAjaxElement('query_results');

        ajaxEngine.registerRequest('showList', '/item/showList');
        ajaxEngine.registerRequest('addToList', '/item/addToList');
        ajaxEngine.registerRequest('removeFromList', '/item/removeFromList');
        ajaxEngine.registerAjaxElement('shopping_list');

        showList();
      }
    </script>

    <table>
      <tr valign="top">

        <td width="20%">

          <div py:if="not session_is_logged_in">
            <div py:replace="loginBox()"/>
          </div>

          <div class="shopping_list" id="shopping_list" py:if="session_is_logged_in">
            <div class="list_name">Shopping List</div>
          </div>

        </td>
        <td>

          <div py:if="not session_is_logged_in">
            Site welcome message and description goes here.
          </div>

          <div class="find_item" py:if="session_is_logged_in">
            <h4>Find Item</h4>
            <form name="findItem" onsubmit="return findItems()">

              <input type="text" name="query" value="" />

              <input class="standalone" type="submit" name="search"
                value="Search" />

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