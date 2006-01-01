<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - My Shopping Lists</title>
</head>

<body>

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

    <form class="group" action="/list/new" method="post">
      <div class="legend">Create List</div>

      <div class="field">
        <div>
          <span class="legend">Name</span>
          <input type="text" name="name" value="" />
        </div>

        <div class="help">Provide a descriptive name for the new list.</div>
      </div>

      <input class="standalone" TYPE="submit" NAME="newBtn" VALUE="New" />
    </form>
    
</body>
</html>