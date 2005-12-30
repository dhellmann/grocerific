<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific New Item</title>
  </head>

  <body>

    <form class="group" action="/item/add" method="post">

      <div class="field">
        <div>
          <span class="legend">Description</span>
          <input type="text" name="name" value="" py:attrs="{'value':name}" />
        </div>

        <div class="help">Provide a description of the new item.  For example:
          <ul>
            <li>Milk, skim, gallon</li>
            <li>Flour, All-purpose</li>
            <li>Tomatoes, canned, crushed, MyBrand</li>
          </ul>
        </div>
      </div>

      <div class="field">
        <div>
          <span class="legend">Add to shopping list?</span>
          <input py:if="addToList" type="checkbox" name="addToList" checked="" />
          <input py:if="not addToList" type="checkbox" name="addToList" />
        </div>

        <div class="help">Should this item be added to your current
          shopping list?
        </div>
      </div>

      <input class="standalone" TYPE="submit" NAME="addBtn" VALUE="Add" />
    </form>
    
  </body>
</html>