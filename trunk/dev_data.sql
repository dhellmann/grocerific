--
-- $Id$
--
-- Test data used in the development database.
--

-- Create a user
INSERT INTO siteuser (username, password, email, location)
	 VALUES ('doug', 'ntsucks', 'doug@hellfly.net', 'Athens, GA');

-- Add items we can put in the list
INSERT INTO "shopping_item" VALUES(1, 'Carrots, large');
INSERT INTO "shopping_item" VALUES(2, 'Onion, yellow, small');
INSERT INTO "shopping_item" VALUES(3, 'Onion, yellow, medium');
INSERT INTO "shopping_item" VALUES(4, 'Onion, yellow, large');
INSERT INTO "shopping_item" VALUES(5, 'Onion, red, small');
INSERT INTO "shopping_item" VALUES(6, 'Onion, red, medium');
INSERT INTO "shopping_item" VALUES(7, 'Onion, red, large');
INSERT INTO "shopping_item" VALUES(8, 'Milk, skim, 1/2 gallon');
INSERT INTO "shopping_item" VALUES(9, 'Milk, skim, gallon');
INSERT INTO "shopping_item" VALUES(10, 'Apple, Gala');
INSERT INTO "shopping_item" VALUES(11, 'Apple, Red Delicious');
INSERT INTO "shopping_item" VALUES(12, 'Apple, Fuji');
INSERT INTO "shopping_item" VALUES(13, 'Flour, All-purpose');
INSERT INTO "shopping_item" VALUES(14, 'Flour, bread');
INSERT INTO "shopping_item" VALUES(15, 'Cheese, deli, provolone');
INSERT INTO "shopping_item" VALUES(16, 'Cheese, deli, American');
INSERT INTO "shopping_item" VALUES(17, 'Cheese, deli, cheddar');
INSERT INTO "shopping_item" VALUES(18, 'Ham, deli');
INSERT INTO "shopping_item" VALUES(19, 'Cheese, deli');
INSERT INTO "shopping_item" VALUES(20, 'Cheese, cheddar');
INSERT INTO "shopping_item" VALUES(21, 'Tomato');
INSERT INTO "shopping_item" VALUES(22, 'Tomato, canned, crushed');
INSERT INTO "shopping_item" VALUES(23, 'Tomato, canned, whole');
INSERT INTO "shopping_item" VALUES(24, 'Tomato, canned, diced');
INSERT INTO "shopping_item" VALUES(25, 'Tomato, canned, Ro-Tel');
INSERT INTO "shopping_item" VALUES(26, 'Velveeta, low-fat, small');
INSERT INTO "shopping_item" VALUES(27, 'Velveeta, Mexican, small');
INSERT INTO "shopping_item" VALUES(28, 'Cat chow');
INSERT INTO "shopping_item" VALUES(29, 'Cheese, deli, swiss');
INSERT INTO "shopping_item" VALUES(30, 'Bread, sandwich');
INSERT INTO "shopping_item" VALUES(31, 'Pasta, linguini');
INSERT INTO "shopping_item" VALUES(32, 'Pasta, ravioli');
INSERT INTO "shopping_item" VALUES(33, 'Pasta, spaghetti');
INSERT INTO "shopping_item" VALUES(34, 'Banannas');
INSERT INTO "shopping_item" VALUES(35, 'Cereal');
INSERT INTO "shopping_item" VALUES(36, 'Cereal, Captain Crunch');
INSERT INTO "shopping_item" VALUES(37, 'Cereal, Wheat Chex');
INSERT INTO "shopping_item" VALUES(38, 'Cereal, Bran Chex');
INSERT INTO "shopping_item" VALUES(39, 'Cereal, Rice Chex');
INSERT INTO "shopping_item" VALUES(40, 'Cereal, Cheerios');
INSERT INTO "shopping_item" VALUES(41, 'Cheese, gorgonzolla');
INSERT INTO "shopping_item" VALUES(42, 'Cheese, blue');
INSERT INTO "shopping_item" VALUES(43, 'Cheese, gorgonzolla, crumbled');
INSERT INTO "shopping_item" VALUES(44, 'Soda, Coke Zero');
INSERT INTO "shopping_item" VALUES(45, 'Soda, Coke');
INSERT INTO "shopping_item" VALUES(46, 'Soda, Diet Coke');
INSERT INTO "shopping_item" VALUES(47, 'Wine, Syrah');
INSERT INTO "shopping_item" VALUES(48, 'Wine, Pinot Grigio');
INSERT INTO "shopping_item" VALUES(49, 'Wine, Prosecco');
INSERT INTO "shopping_item" VALUES(50, 'Wine, Zinfandel');
INSERT INTO "shopping_item" VALUES(51, 'Wine, Cava');
INSERT INTO "shopping_item" VALUES(52, 'Wine, Cabernet Sauvignon');
INSERT INTO "shopping_item" VALUES(53, 'Bread, french');
INSERT INTO "shopping_item" VALUES(54, 'Tissue, Kleenex');
INSERT INTO "shopping_item" VALUES(55, 'Toilet paper');
INSERT INTO "shopping_item" VALUES(56, 'Cherries');

-- Add default quantities
INSERT INTO "shopping_item_info" VALUES(1, 1, 14, '1');
INSERT INTO "shopping_item_info" VALUES(2, 1, 34, 'small bunch');
INSERT INTO "shopping_item_info" VALUES(3, 1, 16, '1/2 lb');
INSERT INTO "shopping_item_info" VALUES(4, 1, 54, '3');
INSERT INTO "shopping_item_info" VALUES(5, 1, 55, '1');
INSERT INTO "shopping_item_info" VALUES(6, 1, 56, 'small bag');

-- Create a shopping list
INSERT INTO shopping_list (name, user_id) VALUES ('Next Trip', 1);
INSERT INTO shopping_list_item (list_id, item_id, quantity) VALUES ( 1, 1, '3' );
INSERT INTO shopping_list_item (list_id, item_id, quantity) VALUES ( 1, 3, '1' );

