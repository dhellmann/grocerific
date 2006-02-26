<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific Login</title>
  </head>

  <body>
    <script>
      function initialFocus() {
        document.login.username.focus();
      }
      onloads.push(initialFocus);
    </script>

    <h2>Login</h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <form name="login" action="/user/login" method="post">
      <fieldset>
        <legend>Login</legend>
        
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
            <td COLSPAN="2">
              <input class="standalone" TYPE="submit" NAME="loginBtn"
                tabindex="${tabindex.next}"
                VALUE="Login" />
              <input class="cancel_button" TYPE="submit"
                NAME="cancelBtn"
                tabindex="${tabindex.next}"
                VALUE="Cancel" onclick="return handleCancel()" />
            </td>
          </tr>
        </TABLE>
        
        <p>Not already a member?  <a
            href="/user/registration_form">Register here</a></p>
        
      </fieldset>
    </form>
    
  </body>
</html>