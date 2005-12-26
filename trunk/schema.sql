-- $Id$

--
-- Users and their preferences.
--
CREATE TABLE user (
	id			int primary key,
	username	text not null unique,
	password	text not null,
	email		text
);

