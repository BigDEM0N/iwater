# .\app.py

from flask import render_template
from flask_script import Manager
from apps import creat_app
from apps.exts import db
from flask_migrate import Migrate

app = creat_app()
manager = Manager(app=app)


@app.route('/index')
def index():
    return render_template('index.html')


migrate = Migrate(app=app, db=db)
print(app.url_map)

if __name__ == '__main__':
    manager.run()
