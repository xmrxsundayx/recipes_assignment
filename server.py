from flask_app import app
#flask_app folder to the app which is the __init__.py
from flask_app.controllers import users_con, recipes_con  
#add for each controller in controller folder

if __name__=="__main__":
    app.run(debug=True)