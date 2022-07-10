<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:py="http://purl.org/kid/ns#" 
  py:extends="'master.kid'">

  <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" onload="bodyOnLoad()">

    <div py:replace="item[:]"/>

    <fieldset>
      <legend>Ads</legend>
    </fieldset>

  </body>
</html>