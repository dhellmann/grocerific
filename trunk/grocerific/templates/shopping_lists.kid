<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - My Shopping Lists</title>
</head>

<body>

    <h2>My Shopping Lists</h2>

    <table class="listing">
      <thead>
        <tr>
          <th>Name</th>
          <th>Items</th>
        </tr>
      </thead>

      <tbody>
        <tr py:for="shopping_list in shopping_lists">
          <td><a py:attrs="{'href':'/list/%s' % shopping_list.id}"
              py:content="shopping_list.name">Name</a>
          </td>
          <td py:content="shopping_list.getItems().count()">Count</td>
        </tr>
      </tbody>

    </table>

    <form action="/list/new" method="post">
      <fieldset>
        <legend>Create List</legend>

        <field>
          <label for="name">Name</label>
          <input type="text" name="name" value="" />
          <input class="standalone" TYPE="submit" NAME="newBtn"
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
    
</body>
</html>