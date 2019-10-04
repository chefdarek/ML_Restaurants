## SQLite3 Database

- menuitem Table
- recipes Table
- subrecipe Table
- Three insert statements for tests
- have to initialize Tables and one insert in order for successful startup

## Query Functions

- create_tables(database, create_table_sql)
     """ create a table from the create_table_sql statement
    :param conn: sqlite3.connect object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
- insert_record(database, sqlite_insert_query):
    """Insert record into tables 
    it is enforcing non duplicates and raises error
    :param conn: sqlite3.connect object
    :param create_table_sql: a CREATE TABLE statement"""
    
- query_recipe_id(database, sql_query_menu_recipe_id):
    """Query returns menuitem table record by recipe_id
    returns: ALL menu item info"""
    
- recipe_full_print(database, recipe_full_print):
    """Query/Print menuitem, recipe, subrecipe tables for full recipe print out
    :param database: sqlite3.connect
    :param recipe_full_print: takes SQL SELECT statement 
    :returns: tuple of menu_item_id, all recipe info plus subrecipe and
        subrecipe of the subrecipe listed in field subrecipe_subrecipe_1,
        and pandas dataframe of fields and values for all of the above
    returns: ALL menu_item_par, recipe, subrecipe info"""

## NEED TO ADD:

- BEV & INV ITEMS, ANCILLARY

- ADD MENU ITEM, RECIPE, SUBRECIPE wrapper FUNCTIONS

- PULL FROM STORAGE AREA COLUMN INTO RECIPE DATAFRAME PRINT STACK

- GROUP BY STORAGE AREA & RECIPES PER STATION VIEW

- ABILITY TO ADD INGREDIENTS LINES FOR RECIPES AND SUBRECIPES THAT BRINGS IN PREP QTY AND MEASURE

- TEST RECIPES WITH 2 + SUB RECIPES

- FORMAT RECIPE VIEW WITH ROOM FOR PREP INSTRUCTIONS AT THE BOTTOM OF EACH RECIPE

- auto populate alergens from inventory-vendor descriptions
