<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Welcome to Grocerific</title>
</head>

<body>
    <script>
      function initialFocus() {
        document.login.username.focus();
      }
      onloads.push(initialFocus);
    </script>

    <h2>Create a Shopping List You Can Access From Anywhere</h2>
    <h3>Organize it, print it, and shop more quickly</h3>

    <p/>

    <table class="home_table">
      <tr valign="top">
        <td width="50%">
          <center><img class="screenshot" width="380" height="320" src="/static/images/screenshot05.png"/></center>
          
          <div class="signup_box">
            <div class="signup"><a href="/user/registration_form">Sign Up Here, It's Free!</a></div>
          </div>
          
        </td>
        
        <td width="50%">
          
          <h4>Organize</h4>
          
          <p style="padding-left: 2em;">Maintain your list as you
            run out of items.  Create separate lists for special
            occasions, recipies, or recurring items.</p>
          
          <h4>Print</h4>
          
          <p style="padding-left: 2em;">Produce a separate list for
            each store where you shop.  Highlight any coupon
            items.</p>
          
          <h4>Shop</h4>
          
          <p style="padding-left: 2em;">Get in and out of the store
            more quickly.  Only visit aisles you need to.</p>
          
        </td>
      </tr>
    </table>
    
</body>
</html>