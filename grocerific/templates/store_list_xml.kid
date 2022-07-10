<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="store_list" py:if="session_is_logged_in">

    <div py:if="not store_count">(None selected)</div>

    <table py:if="store_count">

      <tr py:for="store in stores">

        <td>
          <a class="action_img" onclick="removeFromList(${store.id})"
            alt="&#10005;">
            <img src="/static/images/icons/cancel.png" />
          </a>
          <a href="/store/${store.store.id}">
            <span class="chain_name" py:content="store.store.name"> Name</span>
            (<span class="city" py:content="store.store.city">City</span>)
          </a>
        </td>

      </tr>
    </table>

  </response>
</ajax-response>
