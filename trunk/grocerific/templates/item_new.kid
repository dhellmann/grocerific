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
      </fieldset>
      
      <fieldset>
        <legend>Personalize</legend>
        
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
                
                <label for="tags">Tags:</label> 
                <input type="text" name="tags" value="" size="70" />
                
                <?python
                user_tags = user.getTagNames()
                ?>
                <div class="suggestion" py:if="user_tags">
                  <label>Your tags:</label>
                  <span py:for="other_tag in user_tags">
                    <a onclick='addTag("${other_tag}")' py:content="other_tag">Other tag</a>
                  </span>
                </div>
                
              </field>
      </fieldset>
            
            <fieldset>
              <legend>Stores</legend>
              
              <table>
                <tr valign="top">
                  <td>
                    <table width="100%" class="form_table">
                      <thead>
                        <tr>
                          <th>Store</th>
                          <th>&nbsp;</th>
                          <th>Aisle</th>
                        </tr>
                      </thead>
                      
                      <tbody>
                        <tr py:for="store_info in user.getStores()">
                          <td>
                            <span class="chain_name"
                              py:content="store_info.store.name">
                              Name
                            </span> 
                          </td>
                          <td>
                            <input type="checkbox"
                              name="store_${store_info.store.id}" 
                              checked=""
                              />
                          </td>
                          <td>
                            <input 
                              class="public"
                              type="text"
                              name="aisle_${store_info.store.id}"
                              value=""
                              />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                  <td>
                    <div class="help" style="float: right;">
                      In what aisle is the item found in each
                      store?  For example:
                      <ul>
                        <li>1</li>
                        <li>Pharmacy</li>
                        <li>Bakery</li>
                      </ul>
                      
                      <p>If an item is not available in a store, leave the
                        aisle blank.</p>
                      
                      <p>If you do not buy this item at a store in the list,
                        disable the store by unchecking the box next to the
                        name of the store.</p>
                      
                    </div>
                    
                  </td>
                </tr>
              </table>

            </fieldset>

      <p/>

        <field>
          <input class="add_button" TYPE="submit" NAME="addBtn"
            VALUE="Add" />

          <input class="cancel_button" TYPE="submit" NAME="cancelBtn"
            VALUE="Cancel" onclick="return handleCancel()" />
        </field>
    </form>
    
  </body>
</html>