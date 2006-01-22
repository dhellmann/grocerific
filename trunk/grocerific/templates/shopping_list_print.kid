<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="shopping_list.name">List Name</div></title>
  </head>
  
  <body>

    <h2 py:content="shopping_list.name">List Name</h2>

    <fieldset py:if="items_without_aisles">
      <legend>Items without Aisles</legend>

      <table class="listing">
        <thead>
          <tr>
            <th></th>
            <th style="white-space: normal;" py:for="store in stores" py:content="store">Store</th>
          </tr>
        </thead>
        <tbody>
          <tr py:for="item_info in items_without_aisles">
            <td style="white-space: nowrap;">
              &#10063;
              <a href="/item/${item_info.item.id}" py:content="item_info.item.name">Item</a>
              (<span py:content="item_info.quantity">Quantity</span>)
              <span py:if="item_info.have_coupon">&#9986;</span>
            </td>
            <td py:for="store in stores">&nbsp;</td>
          </tr>
        </tbody>
      </table>
      
    </fieldset>

    <fieldset py:for="(store_name, items_by_aisle) in
      items_in_stores">
      <legend py:content="store_name">Store Name</legend>

      <div class="aisle_list" py:for="(aisle, items) in items_by_aisle">
        <span class="aisle_title" py:content="aisle + ':'">Aisle</span>
        <span class="print_item" py:for="item_info in items">
          &#10063;
          <a href="/item/${item_info.item.id}"
            py:content="item_info.item.name">Item</a>
          (<span py:content="item_info.quantity">Quantity</span>)
          <span py:if="item_info.have_coupon">&#9986;</span>
        </span>
      </div>
      <p/>
    </fieldset>

    <p class="print_links">
      <a href="/list/${shopping_list.id}">Edit this list</a>
      <br/>
      <a href="/list/${shopping_list.id}/prepare_print">Change stores</a>
    </p>

  </body>
</html>