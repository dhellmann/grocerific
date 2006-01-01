<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific New Item</title>
  </head>

  <body>

    <form
      action="/item/edit"
      py:attrs="{'action':'/item/%s/edit' % shopping_item.id}"
      method="post">
      <fieldset>
        <legend>Edit: <span py:replace="shopping_item.name">Item Name</span></legend>

        <field>
          <label for="usuallyBuy">When I buy this, I usually buy:</label> 
          <input type="text" name="usuallyBuy" value="1"
            py:attrs="{'value':shopping_item.getUserInfo(user).usuallybuy}" />
          <div class="help">For example:
            <ul>
              <li>1/2 gallon</li>
              <li>1 lb</li>
              <li>small bunch</li>
            </ul>
          </div>
        </field>

        <field>
          <input class="standalone" TYPE="submit" NAME="editBtn" VALUE="Edit" />

          <input class="standalone" TYPE="submit" NAME="cancelBtn"
            VALUE="Cancel" onclick="return handleCancel()" />
        </field>
      </fieldset>
    </form>

    <p>Add a
      <a py:attrs="{'href':'/item/new_form?name=%s' % shopping_item.name}">related item</a>
    </p>

    <fieldset>
      <legend>Stores</legend>
      
      <p>Set the aisle locations for each of your frequently used stores.</p>
    </fieldset>

  </body>
</html>