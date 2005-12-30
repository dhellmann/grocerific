<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="query_results"
    py:if="session_is_logged_in">

    <div py:if="shopping_item_count" class="query_result" py:for="shopping_item in shopping_items">
      <a class="action_link" 
        title="Add to list" 
        onclick="addToList(%s)"
        py:attrs="{'onclick':'addToList(%s)' % shopping_item.id}">+</a>
      <a py:attrs="{'href':'/item/%s' % shopping_item.id}" py:content="shopping_item.name">Item name</a>
    </div>

    <div py:if="not shopping_item_count" class="query_result">
      No match found
    </div>

  </response>
  <response type="element" id="query_results"
    py:if="not session_is_logged_in">
    <div class="query_result">Log in to search</div>
  </response>
</ajax-response>
