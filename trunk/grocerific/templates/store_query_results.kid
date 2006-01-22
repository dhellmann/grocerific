<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="query_results"
    py:if="session_is_logged_in">

    <div py:if="store_count" class="query_result" py:for="store in stores">
      <a title="Add to my list" 
        onclick="addToList(${store.id})"
        >
        <span class="chain_name" py:content="store.name">Name</span>
        (<span class="city" py:content="store.city">City</span>)
      </a>
    </div>

    <div py:if="not store_count" class="query_result">
      No match found
    </div>

  </response>
  <response type="element" id="query_results"
    py:if="not session_is_logged_in">
    <div class="query_result">Log in to search</div>
  </response>
</ajax-response>
