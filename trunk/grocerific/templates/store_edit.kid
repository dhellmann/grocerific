<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="store.chain">store
        chain</div> @ <div py:replace="store.location">location</div></title>
  </head>

  <body>

    <h2><div py:replace="store.chain">store chain</div> 
      @ <div py:replace="store.location">location</div>
    </h2>

    <fieldset>
      <legend>Edit Store</legend>

      <form method="post"
        py:attrs="{'action':'/store/%s/edit' % store.id}" 
        >
        <field>
          <table class="form_table">
            <tr>
              <td><label for="chain">Chain</label></td>
              <td><input type="text" name="chain" py:attrs="{'value':store.chain}" /></td>
            </tr>
            <tr>
              <td><label for="city">City</label></td>
              <td><input type="text" name="city" py:attrs="{'value':store.city}" /></td>
            </tr>
            <tr>
              <td><label for="location">Location</label></td>
              <td><input type="text" name="location" py:attrs="{'value':store.location}" /></td>
            </tr>
          </table>
        </field>
        
        <field>
          <input class="standalone" type="submit" name="editBtn" value="Save" />
          <input class="standalone" type="submit" name="cancelBtn"
            value="Cancel" onclick="return handleCancel()" />
        </field>
      </form>

    </fieldset>

  </body>
</html>