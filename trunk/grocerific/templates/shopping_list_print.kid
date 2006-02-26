<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
  py:extends="'master.kid'">
  
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="shopping_list.name">List Name</div></title>
  </head>
  
  <body>
    
    <h2 py:content="shopping_list.name">List Name</h2>

    <?python
    #
    # Organize the items into separate lists
    # for each column.
    #
    left = []
    right = []
    i = 0
    for (store_name, items_by_aisle) in items_by_store_and_aisle:
      if i % 2:
        right.append( (store_name, items_by_aisle) )
      else:
        left.append( (store_name, items_by_aisle) )
      i += 1
    #
    # Merge the left and right lists back together
    #
    columnified_lists = map(None, left, right)
    ?>
    <table class="store_lists" width="100%">
      <tr py:for="(left_store, right_store) in columnified_lists" valign="top">

        <td width="50%">
          <?python
          if left_store:
            store_name, items_by_aisle = left_store
          ?>
          <fieldset py:if="left_store">
            <legend py:content="store_name">Store Name</legend>
      
            <table class="aisle_list">
              <tr py:for="(aisle, items) in items_by_aisle">
                <th py:content="aisle + ':'">Aisle</th>
                <td>
                  <div class="print_item" py:for="item in items">
                    &#10063;
                    <a href="/item/${item.id}"
                      target="_blank"
                      py:content="item.name">Item</a>
                    (<span py:content="item.quantity">Quantity</span>)
                    <span py:if="item.have_coupon">&#9986;</span>
                    <span py:if="aisle ==
                      'Unknown'"><u>_____</u></span>
                  </div>
                </td>
              </tr>
            </table>
          </fieldset>
        </td>

        <td width="50%">
          <?python
          if right_store:
            store_name, items_by_aisle = right_store
          ?>
          <fieldset py:if="right_store">
            <legend py:content="store_name">Store Name</legend>
      
            <table class="aisle_list">
              <tr py:for="(aisle, items) in items_by_aisle">
                <th py:content="aisle + ':'">Aisle</th>
                <td>
                  <div class="print_item" py:for="item in items">
                    &#10063;
                    <a href="/item/${item.id}"
                      target="_blank"
                      py:content="item.name">Item</a>
                    (<span py:content="item.quantity">Quantity</span>)
                    <span py:if="item.have_coupon">&#9986;</span>
                    <span py:if="aisle == 'Unknown'"><u>_____</u></span>
                  </div>
                </td>
              </tr>
            </table>
          </fieldset>
        </td>

      </tr>
    </table>

    <p class="print_links">
      <a class="action_link" onclick="window.print()">Print!</a>
      <br/>
      <a href="/list/${shopping_list.id}">Edit this list</a>
      <br/>
      <a href="/list/${shopping_list.id}/prepare_print">Change
        stores</a>
    </p>
    
  </body>
</html>
