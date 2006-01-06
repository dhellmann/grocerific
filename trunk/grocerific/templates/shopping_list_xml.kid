<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="shopping_list" py:if="session_is_logged_in">

    <center py:if="not shopping_list_items.count()">(Empty)</center>
    
    <table class="form_table" valign="top"
      py:if="shopping_list_items.count()">
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
              py:attrs="{'onclick':'removeFromList(%s)' %
              item.id}">&#10005;</a>
            &nbsp;
            <a py:attrs="{'href':'/item/%s' % item.item.id}"
              py:content="item.item.name">Item Name</a>
          </td>
          <td>&nbsp;<a title="Click to change"
              py:attrs="{'id':'quantity_%s' % item.id,
              'onclick':'updateQuantity(%s, &quot;%s&quot;)' % (item.id, item.quantity)}" 
              py:content="item.quantity">Quantity</a>
          </td>
          <td>
            <div py:strip="True" py:if="not item.have_coupon">
              &#10063;
            </div>
            <div py:strip="True" py:if="item.have_coupon">
              &#9986;
            </div>
          </td>
        </tr>
      </tbody>

    </table>

  </response>
</ajax-response>
