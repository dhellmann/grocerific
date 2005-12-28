<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="query_results"
    py:if="session_is_logged_in">
    
    <div class="query_result" py:for="item in items">
      <a class="action_link" 
        title="Add to list" 
        onclick="addToList(%s)"
        py:attrs="{'onclick':'addToList(%s)' % item.id}">+</a>
      <span py:replace="item.name">Item name</span>
    </div>

  </response>
</ajax-response>
