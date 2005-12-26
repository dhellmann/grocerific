<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Welcome to Grocerific</title>
</head>

<body>
    <div align="right" py:if="session_is_logged_in"><a
        href="user/logout">Log Out</a></div>

    <table width="100%">
      <tr><td>&nbsp;</td><td><div style="menu_bar">Menu Goes Here</div></td></tr>
      <tr valign="top">
        <td width="15%">
          <p py:if="not session_is_logged_in"><div py:replace="loginBox()"/></p>
        </td>
        <td>
          Main body goes here!
        </td>
      </tr>
    </table>
    
</body>
</html>