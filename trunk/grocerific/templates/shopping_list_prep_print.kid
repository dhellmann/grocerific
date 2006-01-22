<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="shopping_list.name">List Name</div></title>
</head>

<body>

    <h2 py:content="shopping_list.name">List Name</h2>

    <fieldset>
      <legend>Stores</legend>

      <form action="printable" method="get">

        <div py:for="store in stores">
          <field>
            <input type="checkbox" name="store_${store.id}" />
            <label for="store_${store.id}" py:content="store.name">Store
              Name</label>
          </field>
        </div>

        <p/>

        <input class="standalone" TYPE="submit" NAME="printBtn"
          VALUE="Generate Printable List" />

        <input class="standalone" TYPE="submit" NAME="cancelBtn"
          VALUE="Cancel" onclick="return handleCancel()" />

      </form>

    </fieldset>

</body>
</html>