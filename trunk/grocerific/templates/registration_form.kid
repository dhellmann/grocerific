<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific User Registration</title>
  </head>

  <body>

    <h2>Register</h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <form action="/user/register" method="post">
      <fieldset>
        <legend>Create an Account</legend>

        <TABLE class="form_table">
          <tr>
            <td><label for="username">Username:</label></td>
            <td><input type="text" name="username" value="" /></td>
          </tr>
          <tr>
            <td><label for="password">Password:</label></td>
            <td><input type="password" name="password" value="" /></td>
          </tr>
          <tr>
            <td><label for="email">Email:</label></td>
            <td><input type="text" name="email" value="" /></td>
          </tr>
          
          <tr>
            <td><label for="location">City:</label></td>
            <td><input type="text" name="location" value="" /> </td>
          </tr>
          
          <tr>
            <td COLSPAN="2"><input class="standalone" TYPE="submit"
                NAME="registerBtn" VALUE="Sign Up" /></td>
          </tr>
        </TABLE>

      </fieldset>
    </form>
    
  </body>
</html>