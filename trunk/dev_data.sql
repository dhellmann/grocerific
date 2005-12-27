--
-- $Id$
--
-- Test data used in the development database.
--

-- Create a user
INSERT INTO siteuser (username, password, email) VALUES ('doug', 'ntsucks', 'doug@hellfly.net');

-- Create a shopping list
INSERT INTO shopping_list (name, user_id) VALUES ('Next Trip', 1);

-- Add items we can put in the list
INSERT INTO shopping_item (name) VALUES ( 'Carrots, large');
INSERT INTO shopping_item (name) VALUES ( 'Onion, yellow, small');
INSERT INTO shopping_item (name) VALUES ( 'Onion, yellow, medium');
INSERT INTO shopping_item (name) VALUES ( 'Onion, yellow, large');
INSERT INTO shopping_item (name) VALUES ( 'Onion, red, small');
INSERT INTO shopping_item (name) VALUES ( 'Onion, red, medium');
INSERT INTO shopping_item (name) VALUES ( 'Onion, red, large');
INSERT INTO shopping_item (name) VALUES ( 'Milk, skim, 1/2 gallon');

-- Add items to the list
INSERT INTO shopping_list_item (list_id, item_id, quantity) VALUES ( 1, 1, '3' );
INSERT INTO shopping_list_item (list_id, item_id, quantity) VALUES ( 1, 3, '1' );

