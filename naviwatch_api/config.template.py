import os


""" MariaDB/MySQL database options """
DATABASE = {'host': "localhost",
            'port': 3306,
            'database': "somedatabase",
            'username': "somepassword",
            'password': "somepassword"}

""" Database """
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s/%s?host=%s?port=%s" % (DATABASE['username'], DATABASE['password'],
                                                                           DATABASE['host'], DATABASE['database'],
                                                                           DATABASE['host'], DATABASE['port'])
SQLALCHEMY_POOL_RECYCLE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

""" Flask Options """
FLASK_DEBUG = True
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5055

""" Swagger Options """
SWAGGER_HOST = "{}:{}".format("localhost", FLASK_PORT)
