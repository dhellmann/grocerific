<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="query_results"
    py:if="session_is_logged_in">

    <p>Didn't find what you were looking for?  
      <a href="/item/add_form">Add it now!</a>
    </p>
    
    <div py:if="item_count" class="query_result" py:for="item in items">
      <a class="action_link" 
        title="Add to list" 
        onclick="addToList(%s)"
        py:attrs="{'onclick':'addToList(%s)' % item.id}">+</a>
      <span py:replace="item.name">Item name</span>
    </div>

    <div py:if="not item_count" class="query_result">
      No match found
    </div>

  </response>
</ajax-response>
