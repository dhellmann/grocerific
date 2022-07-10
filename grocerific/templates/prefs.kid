<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific User Preferences</title>
  </head>

  <body>
    <script>
      function initialFocus() {
        document.edit_prefs.password.focus();
      }
      onloads.push(initialFocus);
    </script>

    <h2>Settings for <span py:content="user.username">user</span></h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <form name="edit_prefs" action="/user/edit_prefs" method="post">
      <fieldset>
        <legend>Preferences</legend>

        <table class="form_table">
          
          <tr>
            <td><label for="username">Username:</label> </td>
            <td><span id="username"
                py:content="user.username">username</span></td>
          </tr>

          <tr>
            <td> <label for="password">Password:</label></td>
            <td><input type="password" name="password" value="${user.password}" /></td>
          </tr>

          <tr>
            <td><label for="email">Email:</label></td>
            <td><input type="text" name="email" value="${user.email}" /></td>
          </tr>

          <tr>
            <td><label for="location">City:</label></td>
            <td><input type="text" name="location"
                value="${user.location}" /></td>
          </tr>
        </table>

        <field>
          <input class="icon_button save_btn" TYPE="submit" NAME="editBtn" VALUE="Save" />

          <input class="cancel_button" TYPE="submit" NAME="cancelBtn"
            VALUE="Cancel" onclick="return handleCancel()" />
        </field>

      </fieldset>
      
    </form>
    
  </body>
</html>