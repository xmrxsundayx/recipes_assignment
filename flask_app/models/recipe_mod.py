from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import users_mod
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

class Recipes:
    DB = "recipes_sc"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posting_user = None


    @classmethod
    def save(cls, data):
        query ="""
                    INSERT INTO
                    recipes(user_id, name, description, instructions, date_cooked, under)
                    VALUES
                    (%(user_id)s,%(name)s,%(description)s,%(instructions)s,%(date_cooked)s,%(under)s)
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        # print(result)
        return result

    @classmethod
    def get_all(cls):
        query="""
                    SELECT * FROM
                    recipes
                    JOIN
                    users
                    ON
                    recipes.user_id = users.id
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query)
        all_recipes =[]
        for row in result: 
            one_recipe = cls(row)
            posting_user = ({
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
        })
            one_recipe.posting_user = users_mod.Users(posting_user)
            all_recipes.append(one_recipe)
        return all_recipes


    @classmethod
    def get_by_id(cls,data):
        query="""
                    SELECT * FROM
                    recipes
                    JOIN
                    users
                    ON
                    recipes.user_id = users.id
                    WHERE
                    recipes.id = %(id)s
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        for row in result: 
            one_recipe = cls(row)
            posting_user ={
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
        }
            one_recipe.posting_user = users_mod.Users(posting_user)
            print(one_recipe.posting_user.first_name)
        return one_recipe

    @classmethod
    def get_recipe(cls,data):
        query="""
                    SELECT * FROM
                    recipes
                    WHERE
                    id = %(id)s
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])

    @classmethod
    def edit(cls,data):
        query = """UPDATE recipes 
                SET name=%(name)s,
                description=%(description)s,instructions=%(instructions)s,date_cooked=%(date_cooked)s,under=%(under)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, recipe_id):
        query="""
                    DELETE FROM 
                    recipes
                    WHERE
                    recipes.id =%(id)s
                    ;"""
        data = { 'id': recipe_id}
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result


    @staticmethod
    def verify_recipe(data):
        is_valid =True
        if len(data['name'])<3:
            flash('Name is required')
            is_valid = False
        if len(data['description'])<3:
            flash('Description is required')
            is_valid = False
        if len(data['instructions'])<3:
            flash('Instructions are required')
            is_valid = False
        return is_valid