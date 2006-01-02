<ajax-response xmlns:py="http://purl.org/kid/ns#">
  <response type="element" id="store_list" py:if="session_is_logged_in">

    <div py:if="not stores.count()">(None selected)</div>

    <table py:if="stores.count()">

      <tr py:for="store in stores">

        <td>
          <a py:attrs="{'href':'/store/%s' % store.store.id}">
            <span class="chain_name" py:content="store.store.chain">Chain
              Name</span> @ 
            <span class="location" py:content="store.store.location">Location</span>
            (<span class="city" py:content="store.store.city">City</span>)
          </a>
        </td>

        <td>
          <input type="submit" class="standalone" name="removeBtn" value="Remove"
            py:attrs="{'onclick':'removeFromList(%s)' % store.id}" />
        </td>

      </tr>
    </table>

  </response>
</ajax-response>
