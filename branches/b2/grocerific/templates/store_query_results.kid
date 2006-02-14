<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="object" id="queryResultsManager"
    py:if="session_is_logged_in">

    <store py:for="store in stores" 
      id="${store.id}" description="${store.name}"
      city="${store.city}"
      py:content="store.name">Name</store>

  </response>
</ajax-response>
