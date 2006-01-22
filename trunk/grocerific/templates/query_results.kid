<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="query_results"
    py:if="session_is_logged_in">

    <div py:if="shopping_item_count" class="query_result" py:for="shopping_item in shopping_items">
      <a title="Add to list"
        onclick="addToList(${shopping_item.id})"
        py:content="shopping_item.name">Item name
      </a>

      <small><a title="Details" href="/item/${shopping_item.id}">(details)</a></small>
    </div>

    <div py:if="not shopping_item_count" class="query_result">
      No match found for "<div py:replace="query_string">query string</div>".
    </div>

  </response>
  <response type="element" id="query_results"
    py:if="not session_is_logged_in">
    <div class="query_result">Log in to search</div>
  </response>
</ajax-response>
