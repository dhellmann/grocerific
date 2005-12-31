<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:py="http://purl.org/kid/ns#" 
  py:extends="sitetemplate">

  <head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'">
    <!-- AJAX support libraries -->
    <script src="/static/javascript/prototype.js" />
    <script src="/static/javascript/rico.js" />

    <!-- MochiKit -->
    <script src="/static/javascript/MochiKit/MochiKit.js" />

    <!-- CSS -->
    <link rel="stylesheet" type="text/css" media="all"
      href="/static/css/grocerific.css" />

    <div py:replace="item[:]"/>
  </head>

  <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'">
    <h1>Grocerific</h1>

    <div align="right" py:if="session_is_logged_in">
      <span py:content="session_user">Username</span>
      <a href="/user/prefs">Preferences</a>
      <a href="/user/logout">Log Out</a>
    </div>

    <div style="menu_bar"><a href="/">Home</a> <a href="/list">Next Trip</a></div>
    
    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <div py:def="loginBox()">
      <!-- LOGIN BOX -->
      <form class="group" action="/user/login" method="post">
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
        </TABLE>

        <p>Not already a member?  <a href="/user/registration_form">Register here</a></p>
      </form>

    </div>
    
    <div py:replace="item[:]"/>
  </body>
</html>