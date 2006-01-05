<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="shopping_item.name">item name</div></title>
  </head>

  <body>

    <h2 py:content="shopping_item.name">Item Name</h2>

    <form
      action="/item/edit"
      py:attrs="{'action':'/item/%s/edit' % shopping_item.id}"
      method="post">
      <fieldset>
        <legend>Personalize</legend>

        <field>
          <label for="usuallyBuy">When I buy <span
              py:content="shopping_item.name">this</span>, I usually buy:</label> 
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
    </fieldset>

      <fieldset>
        <legend>Stores</legend>
        
        <table class="form_table">
          <tr>
            <th>Store</th>
            <th>Aisle</th>
          </tr>

          <tr py:for="aisle_info in shopping_item.getAisles(user)">
            <td>
              <span class="chain_name" py:replace="aisle_info.store.chain">Chain Name</span> 
              @ 
              <span class="location" py:replace="aisle_info.store.location">Location</span>
            </td>
            <td>
              <input 
                type="text"
                py:attrs="{'name':'aisle_%s' % aisle_info.store.id,
                'value':aisle_info.aisle}" />
            </td>
          </tr>
        </table>
        <div class="help">In what aisle is the item found in each
          store?  For example:
          <ul>
            <li>1</li>
            <li>Pharmacy</li>
            <li>Bakery</li>
          </ul>
          If an item is not available in a store, leave the aisle blank.
        </div>
      </fieldset>

      <p/>

      <field>
        <input class="standalone" TYPE="submit" NAME="editBtn" VALUE="Edit" />
        
        <input class="standalone" TYPE="submit" NAME="cancelBtn"
          VALUE="Cancel" onclick="return handleCancel()" />
      </field>

    </form>

    <p/>

    <form action="/item/new_form">
      <field>
        <input type="hidden" name="name" py:attrs="{'value':shopping_item.name}"
          value="" />
        <input class="standalone" type="submit" name="addRelatedBtn"
          value="Define a related item" />
      </field>
    </form>

  </body>
</html>