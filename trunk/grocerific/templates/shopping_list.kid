<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="shopping_list" py:if="session_is_logged_in">
    <div class="list_name" py:content="shopping_list.name">List Name</div>
    <center py:if="not shopping_list_items.count()">(Empty)</center>
    
    <table valign="top" width="100%" py:if="shopping_list_items.count()">
      <tr valign="top" class="list_item" py:for="item in shopping_list_items">
        <td><a class="action_link"
            title="Remove from list"
            py:attrs="{'onclick':'removeFromList(%s)' % item.id}">-</a>
        </td>
        <td><a py:attrs="{'href':'/item/%s' % item.item.id}" py:content="item.item.name">Item Name</a></td>
        <td>&nbsp;<a title="Click to change"
            py:attrs="{'id':'quantity_%s' % item.id,
                       'onclick':'updateQuantity(%s, &quot;%s&quot;)' % (item.id, item.quantity)}" 
            py:content="item.quantity">Quantity</a>
        </td>
      </tr>
    </table>

  </response>
</ajax-response>
