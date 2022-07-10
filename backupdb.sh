#!/bin/sh
#
# $Id$
#
# Back up the database.
#
# We only want the INSERT statements (not the CREATE TABLE statements)
#
echo '.dump' | sqlite3 grocerific.db | grep "INSERT INTO" > dev_data.sql
