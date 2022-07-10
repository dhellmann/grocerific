<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"
      py:replace="''"/>
    <meta http-equiv="refresh" content="300" />
    <title>Grocerific User List</title>
    <meta http-equiv="refresh" content="600" py:replace="''"/>
  </head>

  <body>
    
    <h2>Users</h2>
    
    <table class="listing">
      <tr>
        <th>Id</th>
        <th>Username</th>
        <th>Password</th>
        <th>Email</th>
      </tr>
      
      <tr py:for="user in users">
        <td align="right">$user.id</td>
        <td>$user.username</td>
        <td>$user.password</td>
        <td>$user.email</td>
      </tr>
      
    </table>
    
  </body>
</html>
