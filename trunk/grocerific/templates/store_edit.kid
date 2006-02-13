<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'adwords_below.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="store.chain">store
        chain</div> @ <div py:replace="store.location">location</div></title>
  </head>

  <body>

    <h2>
      <div py:replace="store.name">store name</div>
    </h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <form method="post"
      action="/store/${store.id}/edit"
      >
      
      <fieldset py:if="editable">
        <legend>Store Details</legend>
        <field>
          <table class="form_table">
            <tr>
              <td><label for="chain">Chain</label></td>
              <td><input class="public" type="text" size="80" name="chain" value="${store.chain}" /></td>
            </tr>
            <tr>
              <td><label for="location">Location</label></td>
              <td><input class="public" type="text" size="80" name="location" value="${store.location}" /></td>
            </tr>
            <tr>
              <td><label for="city">City</label></td>
              <td><input class="public" type="text" size="80" name="city" value="${store.city}" /></td>
            </tr>
          </table>
        </field>

      </fieldset>
    </form>

    <p/>
    <field>
      <input class="icon_button save_btn" type="submit" name="editBtn" value="Save" />
      <input class="cancel_button" TYPE="submit" NAME="cancelBtn"
        VALUE="Cancel" onclick="return handleCancel()" />
    </field>

    <fieldset py:if="not editable">
      <legend>Store Details</legend>

      <field>
        <table class="form_table">
          <tr>
            <td><label for="chain">Chain</label></td>
            <td py:content="store.chain">Chain</td>
            </tr>
            <tr>
              <td><label for="city">City</label></td>
              <td py:content="store.city">City</td>
            </tr>
            <tr>
              <td><label for="location">Location</label></td>
              <td py:content="store.location">Location</td>
            </tr>
          </table>
        </field>

    </fieldset>

  </body>
</html>