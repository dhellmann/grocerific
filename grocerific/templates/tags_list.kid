<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Grocerific - My Shopping Lists</title>
</head>

<body>

    <h2>My Tags</h2>

    <div py:for="tag_name in tag_names">
      <a href="" py:content="tag_name">Tag Name</a>
    </div>
    
</body>
</html>