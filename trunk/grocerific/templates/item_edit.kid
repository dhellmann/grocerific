<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - <div py:replace="shopping_item.name">item name</div></title>
  </head>

  <body>
    <script>
      function addTag (theTag) {
        var current_value = document.item_edit.tags.value;
        var new_value = current_value + " " + theTag;
        document.item_edit.tags.value = new_value;
      }
    </script>

    <h2 py:content="shopping_item.name">Item Name</h2>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <table width="100%">

      <tr valign="top">
        <td>
          <form name="item_edit"
            action="/item/${shopping_item.id}/edit"
            method="post"  py:if="editable">
            <fieldset>
              <legend>Parameters</legend>
              
              
              <field>
                <label for="name">Description</label>
                <input class="public" type="text" name="name" value="${shopping_item.name}" />
                
                <div class="help">Provide a description of the item.  For example:
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
              <field>
                <label for="usuallyBuy">When I buy this item, I usually buy:</label> 
                <input type="text" name="usuallyBuy"
                  value="${user.getItemInfo(shopping_item).usuallybuy}" />
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
                <input type="text" name="tags" value="$tags" size="70" />
                
                <?python
                user_tags = user.getTagNames()
                ?>
                <div py:if="not user_tags" class="help">For
                  example: TailGate  baby LowCarb</div>
                
                <div class="suggestion" py:if="user_tags">
                  <label>Your tags:</label>
                  <span py:for="other_tag in user_tags">
                    <a onclick='addTag("${other_tag}")' py:content="other_tag">Other tag</a>
                  </span>
                </div>
                
                <?python
                foreign_tags = shopping_item.getForeignTagNames(user)
                ?>
                <div class="suggestion" py:if="foreign_tags">
                  <label>Popular tags:</label>
                  <span py:for="other_tag in foreign_tags">
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
                        <tr py:for="aisle_info in shopping_item.getAisles(user)">
                          <td>
                            <span class="chain_name"
                              py:content="aisle_info.store.name">
                              Name
                            </span> 
                          </td>
                          <td>
                            <input type="checkbox"
                              name="store_${aisle_info.store.id}" 
                              checked=""
                              py:if="aisle_info.store.id in active_store_ids"
                              />
                            <input type="checkbox"
                              name="store_${aisle_info.store.id}" 
                              py:if="not aisle_info.store.id in active_store_ids"
                              />
                          </td>
                          <td>
                            <input 
                              class="public"
                              type="text"
                              name="aisle_${aisle_info.store.id}"
                              value="${aisle_info.aisle}"
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
              <input class="icon_button save_btn" TYPE="submit" NAME="editBtn" VALUE="Save" />
              
              <input class="cancel_button" TYPE="submit" NAME="cancelBtn"
                VALUE="Cancel" onclick="return handleCancel()" />
            </field>
            
          </form>
          
          <fieldset py:if="not editable">
            <legend>Popular Tags</legend>
            <field>
              <?python
              foreign_tags = shopping_item.getForeignTagNames(user)
              ?>
              <div class="suggestion" 
                py:for="other_tag in foreign_tags"
                py:content="other_tag"
                >Foreign Tag
              </div>
            </field>
          </fieldset>
          
          <p/>
          
          <form action="/item/new_form" py:if="editable">
            <field>
              <input type="hidden" name="name" value="${shopping_item.name}" />
              <input class="add_button" type="submit" name="addRelatedBtn"
                value="Define a related item" />
            </field>
          </form>
        </td>

        <td width="20%">
          <fieldset>
            <legend>Ads</legend>
          </fieldset>
        </td>
      </tr>
    </table>

  </body>
</html>
