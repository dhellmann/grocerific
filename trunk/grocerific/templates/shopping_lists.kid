<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - My Shopping Lists</title>
</head>

<body>

    <h2>My Shopping Lists</h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <table width="100%">

      <tr valign="top">

        <td width="50%">
      
          <fieldset>
            <legend>Current Lists</legend>
            <ul>
              
              <li py:for="i, shopping_list in enumerate(shopping_lists)">
                <a href="/list/${shopping_list.id}"
                  py:content="shopping_list.name">Name</a>
                (<span
                  py:content="shopping_list.getItemCount()">Count</span> items)
              </li>
              
            </ul>
          </fieldset>

        </td>

        <td width="100%">

          <form action="/list/new" method="post">
            <fieldset>
              <legend>Create List</legend>
              
              <field>
                <label for="name">Name</label>
                <input type="text" name="name" value="" />
                <input class="add_button" TYPE="submit" NAME="newBtn"
                  VALUE="New" />
                <div class="help">Provide a descriptive name for the new
                  list.  For example:
                  <ul>
                    <li>Tailgate Supplies</li>
                    <li>5 Alarm Chili Ingredients</li>
                    <li>Thanksgiving Menu</li>
                  </ul>
                </div>
              </field>
              
            </fieldset>
          </form>
          
        </td>
      </tr>
    </table>

</body>
</html>
