<ajax-response xmlns:py="http://purl.org/kid/ns#">

  <response type="object" id="queryResultsManager" py:if="session_is_logged_in">
    <shopping_item py:for="shopping_item in shopping_items"
      id="${shopping_item.id}" description="${shopping_item.name}"
      link_icon="&#8592;"
      py:content="shopping_item.name">Name</shopping_item>
  </response>

</ajax-response>
