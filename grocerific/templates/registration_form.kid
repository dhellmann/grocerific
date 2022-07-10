<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific User Registration</title>
  </head>

  <body>
    <script>
      function initialFocus() {
        document.register.username.focus();
      }
      onloads.push(initialFocus);
    </script>

    <h2>Register</h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <form action="/user/register" method="post" name="register">
      <center>
      <fieldset style="width: 50%">
        <legend>Create an Account</legend>

        <TABLE class="form_table">
          <tr>
            <td><label for="username">Username:</label></td>
            <td><input type="text" name="username" value="" tabindex="${tabindex.next}" /></td>
          </tr>
          <tr>
            <td><label for="password">Password:</label></td>
            <td><input type="password" name="password" value="" tabindex="${tabindex.next}" /></td>
          </tr>
          <tr>
            <td><label for="email">Email:</label></td>
            <td><input type="text" name="email" value=""
                tabindex="${tabindex.next}" /></td>
          </tr>
          
          <tr valign="top">
            <td><label for="location">City:</label></td>
            <td><input type="text" name="location" value=""
                tabindex="${tabindex.next}" /> 
              <div class="table_help">This information is used to find
                stores near you.</div>
            </td>
          </tr>
          
          <tr>
            <td COLSPAN="2">
              <input class="add_button" TYPE="submit"
                NAME="registerBtn" VALUE="Sign Up"
                tabindex="${tabindex.next}" />
              <input class="cancel_button" TYPE="submit" NAME="cancelBtn"
                tabindex="${tabindex.next}"
                VALUE="Cancel" onclick="return handleCancel()" />
            </td>
          </tr>
        </TABLE>

      </fieldset>
      </center>
    </form>
    
  </body>
</html>