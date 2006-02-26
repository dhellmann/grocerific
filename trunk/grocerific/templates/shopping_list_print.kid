<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
  py:extends="'master.kid'">
  
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="shopping_list.name">List Name</div></title>
  </head>
  
  <body>
    
    <h2 py:content="shopping_list.name">List Name</h2>
    
    <fieldset py:for="(store_name, items_by_aisle) in items_by_store_and_aisle">
      <legend py:content="store_name">Store Name</legend>
      
      <table class="aisle_list">
        <tr py:for="(aisle, items) in items_by_aisle">
          <th py:content="aisle + ':'">Aisle</th>
          <td>
            <span class="print_item" py:for="item in items">
              &#10063;
              <a href="/item/${item.id}"
                target="_blank"
                py:content="item.name">Item</a>
              (<span py:content="item.quantity">Quantity</span>)
              <span py:if="item.have_coupon">&#9986;</span>
              <span py:if="aisle == 'Unknown'"><u>_____</u></span>
            </span>
          </td>
        </tr>
      </table>
    </fieldset>
    
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
