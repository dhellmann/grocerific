#!/bin/sh
#
# $Id$
#
# Initialize the development database.
#

set -x

DB="grocerific"

#
# Initialize the database with the table structure.
#
tg-admin sql -c prod.cfg create || exit 1

#
# Load some test data.
#
psql $DB < dev_data.sql || exit 1
