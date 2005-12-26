<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific Login</title>
  </head>

  <body>
    
    <form class="group" action="login" method="post">
      <TABLE>
        <tr>
          <th>Username:</th>
          <td><input type="text" name="username" value="" /></td>
        </tr>
        <tr>
          <th>Password:</th>
          <td><input type="password" name="password" value="" /></td>
        </tr>
        <tr>
          <td COLSPAN="2"><input class="standalone" TYPE="submit" NAME="loginBtn" VALUE="Login" /></td>
        </tr>
        <input type="hidden" name="debug" value="1"/>
        <input type="hidden" name="debugOutput" value="1"/>
      </TABLE>
    </form>
  </body>
</html>