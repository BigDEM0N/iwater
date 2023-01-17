# .\app.py


from flask_script import Manager
from apps import creat_app
from apps.exts import db
from flask_migrate import Migrate, MigrateCommand
from apps.user.models import User

app = creat_app()
manager = Manager(app=app)

migrate = Migrate(app=app, db=db)
print(app.url_map)

if __name__ == '__main__':
    manager.run()
