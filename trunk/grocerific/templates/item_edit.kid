<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific New Item</title>
  </head>

  <body>

    <form class="group" action="/item/edit" method="post">
      <div>
        <span class="legend">Description:</span> <span py:content="shopping_item.name">Item</span>
      </div>
      <input type="hidden" name="itemId" value="" py:attr="{'value':shopping_item.id}" />
    </form>

    <h2>Stores</h2>

    <p>Set the aisle locations for each of your frequently used stores.</p>
    
  </body>
</html>