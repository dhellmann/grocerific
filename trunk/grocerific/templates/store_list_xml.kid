<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="store_list" py:if="session_is_logged_in">

    <div py:if="not stores.count()">(None selected)</div>

    <table py:if="stores.count()">

      <tr py:for="store in stores">

        <td>
          <a href="/store/${store.store.id}">
            <span class="chain_name" py:content="store.store.chain">Chain
              Name</span> @ 
            <span class="location" py:content="store.store.location">Location</span>
            (<span class="city" py:content="store.store.city">City</span>)
          </a>
        </td>

        <td>
          <small><a onclick="removeFromList(${store.id})">(remove)</a></small>
        </td>

      </tr>
    </table>

  </response>
</ajax-response>
