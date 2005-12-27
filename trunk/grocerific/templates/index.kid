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

      function onload() {
      ajaxEngine.registerRequest('findItems', '/item/findItems');
      ajaxEngine.registerAjaxElement('query_results');

      ajaxEngine.registerRequest('addToList', '/item/addToList');
      ajaxEngine.registerAjaxElement('shopping_list');
      }
    </script>

    <table>
      <tr valign="top">

        <td width="20%">

          <div py:if="not session_is_logged_in">
            <div py:replace="loginBox()"/>
          </div>

          <div py:if="session_is_logged_in" class="shopping_list">
            <div class="list_name" py:content="shopping_list.name">List Name</div>

            <div id="shopping_list" py:if="not empty_list">
              <table width="100%">
                <tr class="list_item" py:for="item in shopping_list.getItems()">
                  <td py:content="item.item.name">Item Name</td>
                  <td py:content="item.quantity">Quantity</td>
                </tr>
              </table>
            </div>
            
            <div class="list_item"  py:if="empty_list">
              <center>(Empty)</center>
            </div>
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
              <input class="standalone" type="submit" name="search" value="Search" />
              <div class="query_results" id="query_results">
                <table><tr><td>Click to search</td></tr></table>
              </div>
            </form>
          </div>

        </td>
      </tr>
    </table>
    
</body>
</html>