<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific New Store</title>
  </head>

  <body>

    <h2>Define New Store</h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <form action="/store/new" method="post">
      <fieldset>
        <legend>Parameters</legend>

        <field>
          <label for="chain">Chain</label>
          <input class="public" type="text" name="chain" value="${chain}" size="80" />
          
          <div class="help">What chain does the store belong to?  For example:
            <ul>
              <li>Kroger</li>
              <li>Publix</li>
              <li>Earthfare</li>
            </ul>
          </div>
        </field>

        <field>
          <label for="city">City</label>
          <input class="public" type="text" name="city" value="${city}" size="80" />

          <div class="help">Where is this store?</div>
        </field>

        <field>
          <label for="location">Location</label>
          <input class="public" type="text" name="location" value="${location}" size="80" />

          <div class="help">If there is more than one store from the
            same chain in town, where is this specific store?
            <ul>
              <li>China Town</li>
              <li>5th Street</li>
              <li>East-side</li>
            </ul>
          </div>
        </field>


        <field>
          <label>Add to my store list?</label>
          <input type="checkbox" name="addToList" checked="" />

          <div class="help">Should this item be added to your list
            of preferred stores?
          </div>
        </field>

        <field>
          <input class="standalone" TYPE="submit" NAME="addBtn"
            VALUE="Add" />

          <input class="cancel_button" TYPE="submit" NAME="cancelBtn"
            VALUE="Cancel" onclick="return handleCancel()" />
        </field>
      </fieldset>
    </form>
    
  </body>
</html>