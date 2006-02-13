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
    <script src="/static/javascript/MochiKit/MochiKit.js" />

    <!-- CSS -->
    <link rel="stylesheet" type="text/css" media="all"
      href="/static/css/grocerific.css" />
    <link rel="stylesheet" type="text/css" media="print"
      href="/static/css/printer.css" />

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

        /* Call the registered onload callbacks */
        while ( onloads.length > 0 ) {
          callback = onloads.pop();
          callback();
        }
      }
    </script>

    <div class="menu_bar" py:if="session_is_logged_in">
      <span class="sitename">Grocerific</span>

      <div class="menu_bar_r">
        <span py:content="session_user">Username</span> |
        <a href="/user/prefs">Preferences</a> |
        <a href="/user/logout">Logout</a>
      </div>

      <div class="menu_bar_l">
        <a class="menu_item" href="/">Home</a>
        <a class="menu_item" href="/list">Next Trip</a>
        <a class="menu_item" href="/list/lists">My Lists</a>
        <a class="last_menu_item" href="/store/my">My Stores</a>
      </div>
    </div>

    <div class="menu_bar" py:if="not session_is_logged_in">
      <span class="sitename">Grocerific</span>

      <div class="menu_bar_r">
        <a href="/user/login_form">Login</a>
      </div>

      <div class="menu_bar_l">
        <a class="last_menu_item" href="/">Home</a>
      </div>
    </div>
    
    <div py:replace="item[:]"/>

    <div class="footer">
    </div>

  </body>
</html>