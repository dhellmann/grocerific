<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'adwords_below.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="shopping_list.name">List Name</div></title>
</head>

<body>
    <script py:if="editable" src="/static/javascript/query_results.js" />
    <script py:if="editable">

      <!-- Query results manager -->
      var theQueryResultsManager = new QueryResultsManager();

      <!-- Search for items in the database -->
      function findItems() {
        theQueryResultsManager.findItems();
        return false;
      }
      function findItemsByTag(tag) {
        theQueryResultsManager.findItemsByTag(tag);
        return false;
      }

      function browseItems(firstLetter) {
        theQueryResultsManager.browseItems(firstLetter);
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

      <!-- Change the coupon status of an item in the list -->
      function updateCoupon(shoppingListItemId, haveCoupon) {
        ajaxEngine.sendRequest('updateCoupon',
                               "itemId=" + shoppingListItemId,
                               "haveCoupon=" + haveCoupon);
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

      function local_onload() {
        <!-- Set up query results -->
        theQueryResultsManager.registerAJAX();

        <!-- Set up current shopping list -->
        ajaxEngine.registerRequest('showList', '/list/<span py:replace="shopping_list.id">list id</span>/xml');
        ajaxEngine.registerRequest('updateQuantity', '/list/<span py:replace="shopping_list.id">list id</span>/update');
        ajaxEngine.registerRequest('updateCoupon', '/list/<span py:replace="shopping_list.id">list id</span>/coupon');
        ajaxEngine.registerRequest('addToList', '/list/<span py:replace="shopping_list.id">list id</span>/add');
        ajaxEngine.registerRequest('removeFromList', '/list/<span py:replace="shopping_list.id">list id</span>/remove');
        ajaxEngine.registerRequest('importList', '/list/<span py:replace="shopping_list.id">list id</span>/import_list');
        ajaxEngine.registerAjaxElement('shopping_list');

        showList();
      }
      onloads.push(local_onload);

    </script>

    <h2 py:content="shopping_list.name">List Name</h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <table py:if="editable">
      <tr valign="top">

        <td width="50%">
          <fieldset>
            <legend>Contents</legend>

            <div id="shopping_list">loading...</div>

          </fieldset>
        </td>

        <td width="50%">

          <fieldset>
            <legend>Search</legend>
            
            <form name="findItem" onsubmit="return findItems()">
              <field>
                <input type="text" name="query" value="" />
                  
                <input class="standalone" type="submit" name="search"
                  value="Search" />
                
                <input class="standalone" type="submit" name="new"
                  value="Define new item"
                  onclick="return goToNewItem()"
                  />
              </field>

              <p/>

              <field>
                <a py:for="letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#'" 
                  style="margin-left: -1px;"
                  onclick='browseItems("$letter")'
                     py:content="letter"
                     class="action_link">
                    Letter
                  </a>
              </field>
            </form>

            <hr/>

            <field>
              <div class="tag_group">
                <span py:for="tag in user.getTagNames()">
                  <a class="tag_link"
                    onclick='findItemsByTag("$tag")'
                    py:content="tag"
                    >Tag
                  </a>
                </span>
              </div>
            </field>

            <hr/>
            
            <div class="active_message" id="query_message">&nbsp;</div>
            <div id="query_results"></div>
            
          </fieldset>

        </td>

      </tr>
    </table>
    
    <fieldset py:if="editable">
      <legend>Actions</legend>
      
      <field>
        <form method="post"
          action="/list/${shopping_list.id}/clear"
          >
          <input class="standalone" type="submit" name="clearBtn"
            value="Clear this list" />
        </form>
      </field>
      
      <field>
        <form action="/list/${shopping_list.id}/delete"
          method="post"
          py:if="not shopping_list.name == 'Next Trip'">
          <input class="standalone" type="submit" name="deleteBtn"
            value="Delete this list" />
        </form>
      </field>
      
      <field>
        <form py:if="copyable_lists" name="import_form" onsubmit="return importList()">
          <input class="standalone" type="submit" name="copyBtn"
            value="Add contents of" />
          
          <select size="1" id="copyFrom" name="copyFrom">
            <option py:for="other_list in copyable_lists"
              value="${other_list.id}"
              py:content="other_list.name">Name</option>
          </select>
        </form>
      </field>
      
      <field>
        <form action="/list/${shopping_list.id}/prepare_print"
          method="get">
          <input class="standalone" type="submit" name="printBtn"
            value="Print this list" />
        </form>
      </field>
    </fieldset>

    <fieldset py:if="not editable">
      <legend>Contents</legend>

      <field>
        <div py:for="item in shopping_list_items">
          <span py:content="item.item.name">Item</span>
          (<span py:content="item.quantity">Quantity</span>)
          <span py:strip="True" py:if="item.have_coupon">&#9986;</span>
        </div>
      </field>
          
    </fieldset>

</body>
</html>