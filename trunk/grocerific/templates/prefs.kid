<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific User Preferences</title>
  </head>

  <body>

    <form class="group" action="/user/edit_prefs" method="post">
      <TABLE>
        <tr>
          <th>Username:</th>
          <td><span py:content="username">Username</span></td>
        </tr>
        <tr>
          <th>Password:</th>
          <td><input type="password" name="password" value="" 
              py:attrs="{'value':password}" /></td>
        </tr>
        <tr>
          <th>Email:</th>
          <td><input type="text" name="email" value=""
              py:attrs="{'value':email}"  /></td>
        </tr>
        <tr>
          <td COLSPAN="2"><input class="standalone" TYPE="submit" NAME="editBtn" VALUE="Save" /></td>
          </tr>
      </TABLE>
      
    </form>
    
  </body>
</html>