from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST'),
                                             os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        session = self.__session()
        objects = {}
        if cls:
            query = session.query(cls)
            objects = {
                    obj.__class__.__name__ + '.' + obj.id: obj
                    for obj in query.all()
                    }
        else:
            for c in Base.__subclasses__():
                query = session.query(c)
                objects.update({
                    obj.__class__.__name__ + '.' + obj.id: obj
                    for obj in query.all()
                    })
        session.close()
        return objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(
    bind=self.__engine,
    expire_on_commit=False
))


# Initialize DBStorage instance
storage = DBStorage()

storage.reload()
