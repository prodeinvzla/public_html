# db_setup.py
# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from constants import local_db, external_db
# import os
#
# if os.getenv('HOME') == '/home/prodeinvzla':
#     dbtouse = external_db
# else:
#     dbtouse = local_db
#
# engine = create_engine(dbtouse, convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
#
# def init_db():
#     Base.metadata.create_all(bind=engine)