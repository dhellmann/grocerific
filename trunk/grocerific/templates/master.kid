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

    <!-- CSS -->
    <link rel="stylesheet" type="text/css" media="all"
      href="/static/css/grocerific.css" />

    <div py:replace="item[:]"/>
  </head>

  <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" onload="bodyOnLoad()">
    <script>
      function handleCancel() {
        window.history.back();
        return false;
      }

      var onloads = new Array();
      function bodyOnLoad() {
        /* UI effects we want for every page */
        new Rico.Effect.Round('h1', null, null);

        /* Call the registered onload callbacks */
        while ( onloads.length > 0 ) {
          callback = onloads.pop();
          callback();
        }
      }
    </script>

    <h1>Grocerific</h1>

    <div class="menu_bar" py:if="session_is_logged_in">
      <div class="menu_bar_r">
        <span py:content="session_user">Username</span>
        <a href="/user/prefs">Preferences</a>
        <a href="/user/logout">Log Out</a>
      </div>
      <p/>
      <div class="menu_bar_l">
        <a href="/">Home</a>
        <a href="/list">Next Trip</a>
        <a href="/list/lists">My Lists</a>
        <a href="/">My Stores</a>
      </div>
      <p/>
    </div>

    <div class="menu_bar" py:if="not session_is_logged_in">
      <div class="menu_bar_l">
        <a href="/">Home</a>
      </div>
    </div>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <form action="/user/login" method="post" py:def="loginBox()">
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
            <td COLSPAN="2"><input class="standalone" TYPE="submit" NAME="loginBtn" VALUE="Login" /></td>
          </tr>
        </TABLE>
        
        <p>Not already a member?  <a
            href="/user/registration_form">Register here</a></p>
        
      </fieldset>
    </form>
    
    <div py:replace="item[:]"/>
  </body>
</html>