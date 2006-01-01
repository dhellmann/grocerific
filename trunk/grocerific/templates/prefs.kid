<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific User Preferences</title>
  </head>

  <body>

    <form action="/user/edit_prefs" method="post">
      <fieldset>
        <legend>User Preferences</legend>

        <table class="form_table">
          
          <tr>
            <th align="left"><label for="username">Username:</label> </th>
            <td><span id="username"
                py:content="user.username">username</span></td>
          </tr>

          <tr>
            <th align="left"> <label for="password">Password:</label></th>
            <td><input type="password" name="password" value="" 
                py:attrs="{'value':user.password}" /></td>
          </tr>

          <tr>
            <th align="left"><label for="email">Email:</label></th>
            <td><input type="text" name="email" value=""
                py:attrs="{'value':user.email}"  /></td>
          </tr>

          <tr>
            <th align="left"><label for="location">Location:</label></th>
            <td><input type="text" name="location" value=""
                py:attrs="{'value':user.location}"  /></td>
          </tr>
        </table>

        <field>
          <input class="standalone" TYPE="submit" NAME="editBtn" VALUE="Save" />
        </field>

      </fieldset>
      
    </form>
    
  </body>
</html>