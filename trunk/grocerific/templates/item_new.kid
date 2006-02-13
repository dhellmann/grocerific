<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific New Item</title>
  </head>

  <body>

    <h2>Define New Item</h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <form action="/item/add" method="post">
      <fieldset>
        <legend>Parameters</legend>

        <field>
          <label for="name">Description</label>
          <input class="public" type="text" name="name" value="$name" />

          <div class="help">Provide a description of the new item.  For example:
            <ul>
              <li>Milk, skim, gallon</li>
              <li>Flour, All-purpose</li>
              <li>Tomatoes, canned, crushed, MyBrand</li>
            </ul>
          </div>
        </field>


        <field py:if="addToList">
          <label>Add to shopping list?</label>
          <input py:if="addToList" type="checkbox" name="addToList" checked="" />
          <input type="hidden" name="shoppingListId" value="$addToList" />

          <div class="help">Should this item be added to your current
            shopping list?
          </div>
        </field>

        <field>
          <label for="usuallyBuy">When I buy this, I usually buy:</label> 
          <input type="text" name="usuallyBuy" value="1" />
          <div class="help">For example:
            <ul>
              <li>1/2 gallon</li>
              <li>1 lb</li>
              <li>small bunch</li>
            </ul>
          </div>
        </field>

        <field>
          <input class="standalone" TYPE="submit" NAME="addBtn"
            VALUE="Add" />

          <input class="standalone" TYPE="submit" NAME="cancelBtn"
            VALUE="Cancel" onclick="return handleCancel()" />
        </field>
      </fieldset>
    </form>
    
  </body>
</html>