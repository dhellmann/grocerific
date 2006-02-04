<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="shopping_list" py:if="session_is_logged_in">

    <center py:if="not shopping_list_item_count">(Empty)</center>
    
    <table class="form_table" valign="top"
      py:if="shopping_list_item_count">
      <thead>
        <th>Item</th>
        <th>Quantity</th>
        <th>Coupon</th>
      </thead>

      <tbody>
        <tr valign="top" class="list_item" py:for="item in shopping_list_items">
          <td>
            <a class="action_link"
              title="Remove from list"
              onclick="removeFromList(${item.id})"
              >&#10005;</a>
            &nbsp;
            <a href="/item/${item.item.id}"
              py:content="item.item.name">Item Name</a>
          </td>
          <td>&nbsp;<a title="Click to change"
              id="quantity_${item.id}"
              onclick='updateQuantity(${item.id}, "${item.quantity}")'
              py:content="item.quantity">Quantity</a>
          </td>
          <td>
            <div py:strip="True" py:if="not item.have_coupon">
              <a class="coupon_link" title="Click if you have a coupon" onclick="updateCoupon($item.id, 'yes')">&#10063;</a>
            </div>
            <div py:strip="True" py:if="item.have_coupon">
              <a class="coupon_link" title="Click if you do not have a coupon" onclick="updateCoupon($item.id, 'no')">&#9986;</a>
            </div>
          </td>
        </tr>
      </tbody>

    </table>

  </response>
</ajax-response>
