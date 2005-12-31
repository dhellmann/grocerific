<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Welcome to Grocerific</title>
</head>

<body>
    <script>
      function onload() {
      }
    </script>

    <table py:if="not session_is_logged_in">
      <tr valign="top">
        
        <td width="20%">
          <div py:replace="loginBox()"/>
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