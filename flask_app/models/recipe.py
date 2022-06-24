from unittest import result
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash, session

class Recipe:
    db = "recipes_improved"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.under_thirty = int(data["under_thirty"])
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # self.recipe_cook_name = None
        self.recipe_cook = None

    #create - SQL - recipe
    @classmethod
    def create_recipe(cls, data):
        if not cls.validated_recipe(data):
            return False
        query = """
        INSERT INTO recipes 
        (name, description, instructions, date_made, under_thirty, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty)s, %(user_id)s)
        ;"""
        recipe_id=connectToMySQL(cls.db).query_db(query, data)
        return recipe_id
    
    #read - SQL - recipe
    @classmethod
    def get_all_recipes_with_user(cls):
        query = """
        SELECT * FROM recipes
        LEFT JOIN users 
        ON users.id = recipes.user_id
        ;"""
        #returns list of recipe dictionaries with their users appended
        results = connectToMySQL(cls.db).query_db(query)
        all_user_recipe_instances = []
        for db_dictionary_row in results:
            new_recipe = cls(db_dictionary_row)
            # new_recipe.recipe_cook_name = f'{db_dictionary_row["first_name"]} {db_dictionary_row["last_name"]}'
            recipe_cook_dictionary = { 
                "id" :db_dictionary_row['users.id'],
                "first_name":db_dictionary_row['first_name'],
                "last_name": db_dictionary_row['last_name'],
                'email': db_dictionary_row['email'], 
                'password': db_dictionary_row['password'], 
                'created_at': db_dictionary_row["users.created_at"], 
                'updated_at': db_dictionary_row["users.updated_at"]
            }
            new_recipe.recipe_cook = user.User(recipe_cook_dictionary)
            all_user_recipe_instances.append(new_recipe) 
            print("****************", new_recipe)
        return all_user_recipe_instances
    
    @classmethod
    def get_recipe_by_id(cls, id):
        data = {"id" : id}
        query= """
        SELECT * FROM recipes
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = (result[0])
        return result
        

    #update - SQL - recipe
    @classmethod
    def update_recipe_by_id(cls, data):
        if not cls.validated_recipe(data):
            return False
        query= """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, 
        date_made = %(date_made)s, under_thirty = %(under_thirty)s 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = (result[0])
        print("****************** the result is", result) 
        result = connectToMySQL(cls.db).query_db(query, data)
        return True
        
        
        # query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under30=%(under30)s, date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        # return connectToMySQL(cls.db).query_db(query,data)


    #delete - SQL - recipe
    @classmethod
    def delete_recipe_by_id(cls, id):
        data = {"id" : id}
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
        
    #validated 
    @staticmethod
    def validated_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Your recipe name must be at least 3 characters')
            is_valid = False
        if len(data['description']) < 3:
            flash('Your recipe description must be at least 3 characters')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Your recipe instructions must be at least 3 characters')
            is_valid = False
        if data["date_made"] == "":
            flash("Please enter a date")
            is_valid = False
        return is_valid 