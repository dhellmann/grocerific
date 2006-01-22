<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Welcome to Grocerific</title>
</head>

<body>

    <table py:if="not session_is_logged_in">
      <tr valign="top">
        
        <td width="20%">

          <form action="/user/login" method="post">
            <fieldset>
              <legend>Login</legend>
              
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
                  <td COLSPAN="2">
                    <input class="standalone" TYPE="submit" NAME="loginBtn"
                      VALUE="Login" />
                    <input class="standalone" TYPE="submit" NAME="cancelBtn"
                      VALUE="Cancel" onclick="return handleCancel()" />
                  </td>
                </tr>
              </TABLE>
              
              <p>Not already a member?  <a
                  href="/user/registration_form">Register here</a></p>
              
            </fieldset>
          </form>
        </td>

        <td>
          <div py:if="not session_is_logged_in">
            Site welcome message and description goes here.
          </div>
        </td>
      </tr>
    </table>

    <div py:if="session_is_logged_in">
      Need logged-in content here.
    </div>
    
</body>
</html>