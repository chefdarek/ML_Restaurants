import os
# import logging
#
# logging.basicConfig(filename='demolog.log',
#                     level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base
import sqlite3
from sqlite3 import Error
import pandas as pd

from Database.database_startup import create_menuitem_table, create_inventory_table, test_rec_sub_triggers, \
    test_reject_duplicates, create_production_item_table, create_recipes_table, create_subrecipe_table, \
    create_vendor_table


database = r"\\Database\\meal_plan.sqlite"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_local = "sqlite:///D:\\Githubrepos\\meal_plan_mvp\\Database\\meal_plan.sqlite"
    #"sqlite:///{}".format(os.path.join(project_dir, database))
print("Connected to:", database_local)

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = database_local
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(APP)


@APP.route('/', methods=["GET", "POST"])
def landing():
    print("connected to landing")
    if request.method == "POST":
        return render_template("Menu_Item_Card.html")
    return render_template("landing.html")


@APP.route('/menu_item_card', methods=["GET", "POST"])
def menu_item():
    print("connected to menu_item")
    #to check connection to db
    # results = db.session.query(menu_item).all()
    # for r in results:
    #     print(r.menu_item_id)
    if request.method == "POST":
        print(request.form)
        timestampnum = int(request.form.get('timestamp'))
        location_id = str(request.form.get("location_id"))
        menu_item_description = str(request.form.get("menu_title"))
        recipe_name = str(request.form.get("recipe_name"))
        try:
            recipe_name_same = db.session.query(menu_item).filter_by(menu_item_recipe_id=recipe_name).first()
            existing_time = db.session.query(menu_item).filter_by(menu_item_created_on=timestampnum).first()
            menu_item_description_same = db.session.query(menu_item).filter_by(
                menu_item_description=menu_item_description).first()
            if existing_time:
                print("ERROR timestamp, duplicate")
                return render_template("INTEGERROR_menu_item_time.html")
            else:
                pass

            if menu_item_description_same:
                print("ERROR description error, duplicate")
                return render_template("INTEGERROR_menu_item_time_desc.html")
            else:
                pass

            if recipe_name_same:
                print("ERROR recipe name, duplicate")
                return render_template("INTEGERROR_menu_item_time_recipe.html")
            else:
                pass
            new_item = menu_item(menu_item_created_on=timestampnum,
                                 menu_item_location_id=location_id,
                                 menu_item_outlet_id=request.form.get("outlet_id"),
                                 menu_item_recipe_id=request.form.get("recipe_name"),
                                 menu_item_description=request.form.get("menu_title"),
                                 menu_item_subscript=request.form.get("menu_subscription"),
                                 menu_item_pos_name=request.form.get("pos_id"),
                                 menu_item_fire_time=request.form.get("fire_time"),
                                 menu_item_par=request.form.get("par"),
                                 menu_item_dietary=request.form.get("allergen"),
                                 menu_item_menu_price=request.form.get("price"),
                                 menu_item_active_item=request.form.get("activate"),
                                 menu_item_station=request.form.get("station")
                                 )
            db.session.add(new_item)
            db.session.flush()
        except IntegrityError as e:
            db.session.rollback()
            return render_template("INTEGERROR_menu_item.html")
        else:
        #logging.info('look, my new object got primary key %d', new_item.menu_item_id)
            db.session.commit()
            print("Successfully Added New Menu Item")

    return render_template("Menu_Item_Card.html")


@APP.route('/recipe_card', methods=["GET", "POST"])
def recipe_card():
    if request.form:
        print(request.form)
    if request.method == "POST":
        try:
            recipe_name = request.form.get("recipe_name")
            recipe_exists = db.session.query(recipes).filter_by(recipes_recipe_name=recipe_name).first()
            if recipe_exists:
                db.session.rollback()
                print("ERROR Recipe name duplicate")
                return render_template("INTEGERROR_menu_item_time_recipe.html")


            new_recipe = recipes(recipes_recipe_name = request.form.get("recipe_name"),
                                recipes_ingredient_1 = request.form.get("ingredient_1"),
                                recipes_ingredient_prep_1 = request.form.get("prep_1"),
                                recipes_rcp_quantity_1 = request.form.get("qty_1"),
                                recipes_measure_1 = request.form.get("measure_1"),
                                recipes_ingredient_2 = request.form.get("ingredient_2"),
                                recipes_ingredient_prep_2 = request.form.get("prep_2"),
                                recipes_rcp_quantity_2 = request.form.get("qty_2"),
                                recipes_measure_2 = request.form.get("measure_2"),
                                recipes_ingredient_3 = request.form.get("ingredient_3"),
                                recipes_ingredient_prep_3 = request.form.get("prep_3"),
                                recipes_rcp_quantity_3 = request.form.get("qty_2"),
                                recipes_measure_3 = request.form.get("measure_3"),
                                recipes_sub_recipe = request.form.get("subrecipe_1"),
                                recipes_sub_recipe_qty = request.form.get("subqty_2"),
                                recipe_sub_recipe_measure = request.form.get("submeas_1"),
                                recipes_sub_recipe_2=request.form.get("subrecipe_1"),
                                recipes_sub_recipe_qty_2=request.form.get("subqty_2"),
                                recipe_sub_recipe_measure_2 =request.form.get("submeas_1"),
                                recipes_dietary = request.form.get("recipe_dietary"),
                                recipes_prep_instructions = request.form.get("prep_info"),
                                recipes_fire_instructions = request.form.get("fire_info"),
                                recipes_est_prep_time = request.form.get("prep_time"),
                                recipes_recipe_type = request.form.get("prep_time")
                                )
            db.session.add(new_recipe)
            db.session.flush()
            # logging.info('look, my new object got primary key %d', new_item.menu_item_id)
            db.session.commit()
            print("Successfully Added New Menu Item")
        except IntegrityError as e:
            db.session.rollback()
            # print(INtegrity Error)
    return render_template("Recipe_Card.html")


@APP.route('/subrecipe_card', methods=["GET", "POST"])
def subrecipe():
    if request.form:
        print(request.form)
    if request.method == "POST":
        try:
            subrecipe_name = request.form.get("recipe_name")
            recipe_exists = db.session.query(subrecipe).filter_by(subrecipe_recipe_name=subrecipe_name).first()
            if recipe_exists:
                db.session.rollback()
                print("ERROR Recipe name duplicate")
                return render_template("INTEGERROR_menu_item_time_recipe.html")

            new_subrecipe = subrecipe(subrecipe_recipe_name=request.form.get("recipe_name"),
                                 subrecipe_ingredient_1=request.form.get("ingredient_1"),
                                 subrecipe_ingredient_prep_1=request.form.get("prep_1"),
                                 subrecipe_rcp_quantity_1=request.form.get("qty_1"),
                                 subrecipe_ing_measure_1=request.form.get("measure_1"),
                                 subrecipe_ingredient_2=request.form.get("ingredient_2"),
                                 subrecipe_ingredient_prep_2=request.form.get("prep_2"),
                                 subrecipe_rcp_quantity_2=request.form.get("qty_2"),
                                 subrecipe_ing_measure_2=request.form.get("measure_2"),
                                 subrecipe_ingredient_3=request.form.get("ingredient_3"),
                                 subrecipe_ingredient_prep_3=request.form.get("prep_3"),
                                 subrecipe_rcp_quantity_3=request.form.get("qty_2"),
                                 subrecipe_ing_measure_3=request.form.get("measure_3"),
                                 subrecipe_subrecipe_1=request.form.get("subrecipe_1"),
                                 subrecipe_subrecipe_qty_1=request.form.get("subqty_2"),
                                 subrecipe_subrecipe_measure_1=request.form.get("submeas_1"),
                                 subrecipe_dietary=request.form.get("recipe_dietary"),
                                 subrecipe_prep_instructions=request.form.get("prep_info"),
                                 subrecipe_prep_time=request.form.get("prep_time"),
                                 subrecipe_tag=request.form.get("tag")
                                 )
            db.session.add(new_subrecipe)
            db.session.flush()
            # logging.info('look, my new object got primary key %d', new_item.menu_item_id)
            db.session.commit()
            print("Successfully Added New Menu Item")
        except IntegrityError as e:
            db.session.rollback()
            # print(INtegrity Error)
    return render_template("Subrecipe_Card.html")


def create_tables(database, create_table_sql):
    """ create a table from the create_table_sql statement
    :param database: sqlite3.connect object
    :param create_table_sql: a CREATE TABLE statement
    :returns confirmation of table creation:
    """
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(create_table_sql)
        if cursor.rowcount == 0:
            print(f"FAILED: Table {create_table_sql[:30]} failed. rowcount:", cursor.rowcount)
        else:
            print(f"Successfully created table:{create_table_sql[:30]}")


    except Error as e:
        print(e)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def insert_record(database, sqlite_insert_query):
    """Insert record into tables
    it is enforcing non duplicates but NEEDS TO RAISE ERROR FOR DUPLICATE RECORD?? IF Possible"""
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        if cursor.rowcount == 0:
            print(f"FAILED: Record {sqlite_insert_query[:30]} inserted failed. rowcount:", cursor.rowcount)
        else:
            print(f"Record {sqlite_insert_query[:30]} inserted successfully.")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


# --------------------Tables Index Triggers Startups ---------------------#
# menu items are point of sale info items that link recipes to customer facing info
# you cannot create a menu item without a recipe inventory item
menu_item_table = """ CREATE TABLE  menuitem (
                                        menu_item_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                        menu_item_created_on INTEGER UNIQUE NOT NULL,
                                        menu_item_location_id VARCHAR NOT NULL,
                                        menu_item_outlet_id VARCHAR NOT NULL,
                                        menu_item_recipe_id TEXT UNIQUE NOT NULL,
                                        menu_item_description TEXT UNIQUE NOT NULL,
                                        menu_item_subscript TEXT NOT NULL,
                                        menu_item_station VARCHAR(50) NOT NULL,
                                        menu_item_pos_name VARCHAR(25) NOT NULL,
                                        menu_item_fire_time INTEGER NOT NULL,
                                        menu_item_par INTEGER NOT NULL,
                                        menu_item_dietary TEXT,
                                        menu_item_menu_price REAL NOT NULL,
                                        menu_item_active_item BIT);"""

id_create_date_recipe_desc_index = """CREATE UNIQUE INDEX id_create_date_recipe_desc ON menuitem (menu_item_id, menu_item_created_on,
                                                                                 menu_item_recipe_id, menu_item_description);"""
#NOTES ON RECIPES

# recipes are the line item description of menu items
# recipes forces link of ingredients to inventory items through production items
# recipes link to cook view, production item, inventory and purchasing
# recipes will link to subrecipe upon print or view automatically

# !!! need to add recipe tags for genre and attributes for chatbot
recipes_table = """CREATE TABLE  recipes (
                                    recipes_recipe_name TEXT PRIMARY KEY NOT NULL,
                                    recipes_ingredient_1 TEXT NOT NULL,
                                    recipes_ingredient_prep_1 TEXT NOT NULL,
                                    recipes_rcp_quantity_1 REAL NOT NULL,
                                    recipes_measure_1 TEXT NOT NULL,
                                    recipes_ingredient_2 TEXT NOT NULL,
                                    recipes_ingredient_prep_2 TEXT NOT NULL,
                                    recipes_rcp_quantity_2 REAL NOT NULL,
                                    recipes_measure_2 TEXT NOT NULL,
                                    recipes_ingredient_3 TEXT NOT NULL,
                                    recipes_ingredient_prep_3 TEXT NOT NULL,
                                    recipes_rcp_quantity_3 REAL NOT NULL,
                                    recipes_measure_3 TEXT NOT NULL,
                                    recipes_sub_recipe VARCHAR NOT NULL,
                                    recipes_sub_recipe_qty REAL NOT NULL,
                                    recipe_sub_recipe_measure TEXT NOT NULL,
                                    recipes_sub_recipe_2 VARCHAR NOT NULL,
                                    recipes_sub_recipe_qty_2 REAL NOT NULL,
                                    recipe_sub_recipe_measure_2 TEXT NOT NULL,
                                    recipes_dietary TEXT,
                                    recipes_prep_instructions VARCHAR NOT NULL,
                                    recipes_fire_instructions VARCHAR NOT NULL,
                                    recipes_est_prep_time REAL NOT NULL,
                                    recipes_recipe_type VARCHAR NOT NULL,
                                    FOREIGN KEY (recipes_recipe_name) REFERENCES menuitem (menu_item_recipe_id)
                                );"""

id_name_recipe_index = """CREATE UNIQUE INDEX id_recipe_index ON recipes (recipes_recipe_name);"""

recipe_insert_trigger1 = """CREATE TRIGGER ing_aft_insert AFTER INSERT ON recipes BEGIN
                            INSERT INTO production_item  (production_recipe_name, production_item_name,production_prep,production_item_qty, production_measure)
                                VALUES(
                                NEW.recipes_recipe_name, NEW.recipes_ingredient_1, NEW.recipes_ingredient_prep_1,
                                NEW.recipes_rcp_quantity_1, NEW.recipes_measure_1);
                            INSERT INTO production_item (production_recipe_name, production_item_name, production_prep, production_item_qty, production_measure)
                                VALUES(
                                NEW.recipes_recipe_name, NEW.recipes_ingredient_2, NEW.recipes_ingredient_prep_1,
                                NEW.recipes_rcp_quantity_1, NEW.recipes_measure_1);
                             INSERT INTO production_item (production_recipe_name, production_item_name, production_prep, production_item_qty, production_measure)
                                VALUES(
                                NEW.recipes_recipe_name,NEW.recipes_ingredient_3, NEW.recipes_ingredient_prep_3,
                                NEW.recipes_rcp_quantity_3, NEW.recipes_measure_3);
                            END;"""

# subrecipe are items that will never be standalone menu items
subrecipe_table = """CREATE TABLE   subrecipe (
                                    subrecipe_recipe_name TEXT PRIMARY KEY UNIQUE NOT NULL,
                                    subrecipe_ingredient_1 TEXT NOT NULL,
                                    subrecipe_ingredient_prep_1 TEXT NOT NULL,
                                    subrecipe_rcp_quantity_1 REAL NOT NULL,
                                    subrecipe_ing_measure_1 TEXT NOT NULL,
                                    subrecipe_ingredient_2 TEXT NOT NULL,
                                    subrecipe_rcp_quantity_2 REAL NOT NULL,
                                    subrecipe_ingredient_prep_2 TEXT NOT NULL,
                                    subrecipe_ing_measure_2 TEXT NOT NULL,
                                    subrecipe_ingredient_3 TEXT NOT NULL,
                                    subrecipe_rcp_quantity_3 REAL NOT NULL,
                                    subrecipe_ingredient_prep_3 TEXT NOT NULL,
                                    subrecipe_ing_measure_3 TEXT NOT NULL,
                                    subrecipe_subrecipe_1 TEXT,
                                    subrecipe_subrecipe_qty_1 REAL,
                                    subrecipe_subrecipe_measure_1 TEXT,
                                    subrecipe_dietary TEXT NOT NULL,
                                    subrecipe_prep_instructions VARCHAR NOT NULL,
                                    subrecipe_prep_time REAL NOT NULL,
                                    subrecipe_tag TEXT,
                                    FOREIGN KEY (subrecipe_recipe_name) REFERENCES recipes (recipes_sub_recipe)
                                );"""

subrecipe_insert_trigger = """CREATE TRIGGER sub_ing_aft_insert AFTER INSERT ON subrecipe BEGIN
                            INSERT INTO production_item  (production_subrecipe_name, production_item_name,production_prep,production_item_qty, production_measure)
                                VALUES(
                                NEW.subrecipe_recipe_name, NEW.subrecipe_ingredient_1,NEW.subrecipe_ingredient_prep_1,
                                NEW.subrecipe_rcp_quantity_1, NEW.subrecipe_ing_measure_1);
                            INSERT INTO production_item (production_subrecipe_name,production_item_name, production_prep, production_item_qty, production_measure)
                                VALUES(
                                NEW.subrecipe_recipe_name, NEW.subrecipe_ingredient_2,NEW.subrecipe_ingredient_prep_2,
                                NEW.subrecipe_rcp_quantity_2, NEW.subrecipe_ing_measure_2);
                             INSERT INTO production_item (production_subrecipe_name, production_item_name, production_prep, production_item_qty, production_measure)
                                VALUES(
                                NEW.subrecipe_recipe_name, NEW.subrecipe_ingredient_3,NEW.subrecipe_ingredient_prep_3,
                                NEW.subrecipe_rcp_quantity_3, NEW.subrecipe_ing_measure_3);
                            END;"""

subrecipe_name_index = """CREATE UNIQUE INDEX subrecipe_name_index ON subrecipe (subrecipe_recipe_name);"""

# list of all recipe & subrecipe ingredients globally with prep qty and measure with total

production_item_table = """CREATE TABLE production_item (
                            production_item_id INTEGER UNIQUE PRIMARY KEY  NOT NULL,
                            production_recipe_name TEXT DEFAULT "NA",
                            production_subrecipe_name TEXT DEFAULT "NA",
                            production_item_name TEXT NOT NULL,
                            production_prep TEXT NOT NULL,
                            production_item_qty REAL NOT NULL,
                            production_measure TEXT NOT NULL,
                            production_total_qty REAL,
                            production_total_measure TEXT,
                            production_item_storage_loc VARCHAR,
                            FOREIGN KEY (production_recipe_name) REFERENCES recipes (recipes_recipe_name),
                            FOREIGN KEY (production_subrecipe_name) REFERENCES subrecipe (subrecipe_recipe_name)
                            );"""

production_item_unique = """CREATE UNIQUE INDEX production_item_id ON production_item (production_item_id);"""

production_item_inv_trigger = """CREATE TRIGGER prod_aft_insert_invent AFTER INSERT ON production_item BEGIN
                                 INSERT INTO inventory_item (inventory_item_name, inventory_item_qty, inventory_item_measure)
                                     VALUES(NEW.production_item_name, NEW.production_item_qty, NEW.production_measure);
                                 END;"""

# inventory items are triggered from recipe & sub recipe ingredients to link
## CREATE A METHOD OF CONSOLIDATING inventory item to net line items with par and UPDATING vendor item info tags for recommmendations
## python script trigger to prompt for vendor link??
## inventory vendor item id needs to be forced update on linking inv item to vendor and recipe/subrecpe generate
inventory_item_table = """CREATE TABLE inventory_item (
                                            inventory_item_number INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                            inventory_item_name TEXT NOT NULL,
                                            inventory_item_qty REAL NOT NULL,
                                            inventory_item_measure TEXT NOT NULL,          
                                            inventory_storage_location_id VARCHAR,
                                            inventory_par REAL,
                                            inventory_par_measure TEXT,
                                            inventory_vendor_item_id_num INTEGER
                                            );"""

inventory_item_unique_index = """CREATE UNIQUE INDEX inventory_item_unique_number
                                 ON inventory_item (inventory_item_number, inventory_item_name, inventory_item_measure);"""

vendor_item_table = """CREATE TABLE vendor_item_table (
                                            vendor_item_num INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                            vendor_item_description VARCHAR NOT NULL,
                                            vendor_item_ap_count REAL NOT NULL,
                                            vendor_item_ap_count_measure TEXT NOT NULL,
                                            vendor_item_ap_pack TEXT NOT NULL,
                                            vendor_item_ap_qty_order REAL NOT NULL,
                                            vendor_item_glcenter NOT NULL,
                                            vendor_name TEXT NOT NULL,
                                            vendor_item_qrcode VARCHAR UNIQUE NOT NULL,
                                            vendor_allergen_code,
                                            vendor_item_par REAL,
                                            vendor_item_onhand REAL,
                                            vendor_item_cost REAL NOT NULL);"""

vendor_item_unique_index = """CREATE UNIQUE INDEX vendor_item_unique_number
                              ON vendor_item_table (vendor_item_num);"""

# ------------------------------- Query Insert Startups ------------------#
sqlite_menu_insert_query = """INSERT INTO `menuitem`
                          ('menu_item_created_on',
                          'menu_item_location_id',
                          'menu_item_outlet_id',
                          'menu_item_recipe_id',
                          'menu_item_description',
                          'menu_item_subscript',
                          'menu_item_station',
                          'menu_item_pos_name',
                          'menu_item_fire_time',
                          'menu_item_par',
                          'menu_item_dietary',
                          'menu_item_menu_price',
                          'menu_item_active_item') 
                           VALUES 
                          (1570006802,'graduate_seattle','mountaineer','Grilled Chicken','Grilled Free Range Chicken',
                          'mash potato and carrot', 'Grill', 'Grill','12','35','meat, soy, dairy','15.45',1);"""

# format and insert first record on recipes
sqlite_recipe_insert_query = """INSERT INTO 'recipes'
                          ('recipes_recipe_name',
                          'recipes_ingredient_1',
                          'recipes_ingredient_prep_1',
                          'recipes_rcp_quantity_1',
                          'recipes_measure_1',
                          'recipes_ingredient_2',
                          'recipes_ingredient_prep_2',
                          'recipes_rcp_quantity_2',
                          'recipes_measure_2',
                          'recipes_ingredient_3',
                          'recipes_ingredient_prep_3',
                          'recipes_rcp_quantity_3',
                          'recipes_measure_3',
                          'recipes_sub_recipe',
                          'recipes_sub_recipe_qty',
                          'recipe_sub_recipe_measure',
                          'recipes_dietary', 
                          'recipes_prep_instructions',
                          'recipes_fire_instructions',
                          'recipes_est_prep_time') 
                           VALUES 
                          ('Grilled Chicken','chix breast','whole','8','lbs', 'red bliss potato','quartered','4','oz',
                          'carrots', 'sliced', '3', 'oz.wt.','chausuer sauce', '3', 'oz','meat, soy, dairy',
                          '1. wash chicken 2. braise in red wine and stock 4hrs 3. pull sblah blah blah 4. cryovac & chill for service',
                          '1. Grill 4 mins on each side 2. Saute potatos and peppers 3. Spoon chausuer on plate, scoop mash, rest octo leg over, garnish with carrots',
                          '85');"""

# recipe insert trigger test
sqlite_recipe_insert_trigger = """INSERT INTO 'recipes'
                          ('recipes_recipe_name',
                          'recipes_ingredient_1',
                          'recipes_ingredient_prep_1',
                          'recipes_rcp_quantity_1',
                          'recipes_measure_1',
                          'recipes_ingredient_2',
                          'recipes_ingredient_prep_2',
                          'recipes_rcp_quantity_2',
                          'recipes_measure_2',
                          'recipes_ingredient_3',
                          'recipes_ingredient_prep_3',
                          'recipes_rcp_quantity_3',
                          'recipes_measure_3',
                          'recipes_sub_recipe',
                          'recipes_sub_recipe_qty',
                          'recipe_sub_recipe_measure',
                          'recipes_dietary', 
                          'recipes_prep_instructions',
                          'recipes_fire_instructions',
                          'recipes_est_prep_time') 
                           VALUES 
                          ('Grilled EGGS','ostrich eggs','whole','8','ea', 'red bliss asparagus','quartered','4','oz',
                          'carrots', 'sliced', '3', 'oz.wt.','donkey sauce', '3', 'oz','meat, soy, dairy',
                          '1. wash chicken 2. braise in red wine and stock 4hrs 3. pull sblah blah blah 4. cryovac & chill for service',
                          '1. Grill 4 mins on each side 2. Saute potatos and peppers 3. Spoon chausuer on plate, scoop mash, rest octo leg over, garnish with carrots',
                          '85');"""

# format and insert first record on subrecipe
sqlite_subrcp_insert = """INSERT INTO 'subrecipe'
                                    ('subrecipe_recipe_name',
                                    'subrecipe_ingredient_1',
                                    'subrecipe_ingredient_prep_1',
                                    'subrecipe_rcp_quantity_1',
                                    'subrecipe_ing_measure_1',
                                    'subrecipe_ingredient_2',
                                    'subrecipe_ingredient_prep_2',
                                    'subrecipe_rcp_quantity_2',
                                    'subrecipe_ing_measure_2',
                                    'subrecipe_ingredient_3',
                                    'subrecipe_ingredient_prep_3',
                                    'subrecipe_rcp_quantity_3',
                                    'subrecipe_ing_measure_3',
                                    'subrecipe_subrecipe_1',
                                    'subrecipe_subrecipe_qty_1',
                                    'subrecipe_subrecipe_measure_1',
                                    'subrecipe_prep_instructions',
                                    'subrecipe_dietary')
                                    VALUES
                                    ('chausuer sauce','button mushrooms','sliced', '1', 'lb',
                                    'shallot', 'minced','8','oz', 'white wine','pour', '6','oz','demi glace (basic)','1','G',
                                    '1. Saute mushroom & shallot 2.deglaze with white wine 3. Add demi glace and reduce by 1/2',
                                    'meat, gluten'
                                    );"""

# subrecipe insert trigger test
sqlite_subrcp_insert_trigger = """INSERT INTO 'subrecipe'
                                    ('subrecipe_recipe_name',
                                    'subrecipe_ingredient_1',
                                    'subrecipe_ingredient_prep_1',
                                    'subrecipe_rcp_quantity_1',
                                    'subrecipe_ing_measure_1',
                                    'subrecipe_ingredient_2',
                                    'subrecipe_ingredient_prep_2',
                                    'subrecipe_rcp_quantity_2',
                                    'subrecipe_ing_measure_2',
                                    'subrecipe_ingredient_3',
                                    'subrecipe_ingredient_prep_3',
                                    'subrecipe_rcp_quantity_3',
                                    'subrecipe_ing_measure_3',
                                    'subrecipe_subrecipe_1',
                                    'subrecipe_subrecipe_qty_1',
                                    'subrecipe_subrecipe_measure_1',
                                    'subrecipe_prep_instructions',
                                    'subrecipe_dietary')
                                    VALUES
                                    ('donkey sauce','p.cubenesis mushrooms','sliced', '1', 'lb',
                                    'shallittle', 'minced','8','oz', 'white noise','pour', '6','oz','demi glace (basic)','1','G',
                                    '1. Saute mushroom & shallittle 2.deglaze with white wine 3. Add demi glace and reduce by 1/2',
                                    'meat, gluten'
                                    );"""

##format and insert first record on subrecipe where subrecipe has subrecipe
sqlite_subrcp2_insert = """INSERT INTO 'subrecipe'
                                    ('subrecipe_recipe_name',
                                    'subrecipe_ingredient_1',
                                    'subrecipe_ingredient_prep_1',
                                    'subrecipe_rcp_quantity_1',
                                    'subrecipe_ing_measure_1',
                                    'subrecipe_ingredient_2',
                                    'subrecipe_ingredient_prep_2',
                                    'subrecipe_rcp_quantity_2',
                                    'subrecipe_ing_measure_2',
                                    'subrecipe_ingredient_3',
                                    'subrecipe_ingredient_prep_3',
                                    'subrecipe_rcp_quantity_3',
                                    'subrecipe_ing_measure_3',
                                    'subrecipe_subrecipe_1',
                                    'subrecipe_subrecipe_qty_1',
                                    'subrecipe_subrecipe_measure_1',
                                    'subrecipe_prep_instructions',
                                    'subrecipe_dietary')
                                    VALUES
                                    ('demi glace (basic)','beef bones','whole', '10', 'lb',
                                    'water', 'cold','12','G', 'garlic','minced','6','oz','NA','NA','NA',
                                    '1. Rinse Bones 2. Cover with water 3. simmer for 8 hours add garlic 4. After 10 hours strain and cool 5. Bag and cryo',
                                    'meat, gluten'
                                    )"""

if __name__ == "__main__":
    print("pySqlite3", sqlite3.version, "Sqlite3 v.", sqlite3.sqlite_version, "Pandas", pd.__version__)

    # create & test a database connection
    database = r"D:\Githubrepos\meal_plan_mvp\Database\meal_plan.sqlite"
    conn = sqlite3.connect(database)
    c = conn.cursor()
    print("Opened database successfully")

    create_menuitem_table(database, menu_item_table, id_create_date_recipe_desc_index, sqlite_menu_insert_query)
    create_recipes_table(database, recipes_table,   id_name_recipe_index, sqlite_recipe_insert_query)
    create_subrecipe_table(database, subrecipe_table, subrecipe_name_index, sqlite_subrcp_insert, sqlite_subrcp2_insert)
    create_production_item_table(database, production_item_table, production_item_unique, recipe_insert_trigger1,
                                 subrecipe_insert_trigger, production_item_inv_trigger)
    create_inventory_table(database, inventory_item_table, inventory_item_unique_index)
    create_vendor_table(database, vendor_item_table, vendor_item_unique_index)
    test_rec_sub_triggers(database, sqlite_recipe_insert_trigger, sqlite_subrcp_insert_trigger)
    test_reject_duplicates(database, sqlite_menu_insert_query, sqlite_recipe_insert_query, sqlite_subrcp2_insert)


    #Automap Sqlalchemy
    print("create engine")
    engine = create_engine(database_local, echo=True)
    engine.connect()

    # produce our own MetaData object
    metadata = MetaData()
    metadata.reflect(engine)

    Base = automap_base(metadata=metadata)
    Base.prepare(db.engine, reflect=True)
    menu_item, recipes, subrecipe, = Base.classes.menuitem, Base.classes.recipes, Base.classes.subrecipe
    production_item, vendor_item, inventory_item = Base.classes.production_item, Base.classes.vendor_item_table, \
                                                   Base.classes.inventory_item
    # start flask app
    APP.run(debug=True)
