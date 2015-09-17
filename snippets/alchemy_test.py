import sqlalchemy


print sqlalchemy.__version__

from sqlalchemy import create_engine
engine = create_engine('mysql://root:mysql@localhost/cos', echo=True)
engine.execute("select 1").scalar()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(100))
    password = Column(String(100))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name,
                                            self.fullname, self.password)


print User.__table__
print dir(User.__table__)
if User.__table__.exists(engine):
    User.__table__.drop(engine)
    print User.__table__.exists(engine)
else:
    User.__table__.create(engine)
    print User.__table__.exists(engine)
# print User.__mapper__


# print dir(Base)
# print Base.metadata
# print dir(engine)
# print 'begin', engine.begin
# print 'connect', engine.connect
# print 'name', engine.name
# print 'driver', engine.driver
# print 'has_table', engine.has_table
# print 'name', engine.name
# print 'pool', engine.pool
# print 'table_names', engine.table_names
# Base.metadata.create_all(engine)


# ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
# print ed_user.name
# print ed_user.password
# print ed_user.fullname
# print str(ed_user.id)


# from sqlalchemy.orm import sessionmaker

# Session = sessionmaker(bind=engine)
# session = Session()
# session.add(ed_user)
# print dir(session)
# our_user = session.query(User).filter_by(name='ed').first()
# print our_user
# print our_user is ed_user
# # ed_user.password = 'test--'
# print session.query(User).filter_by(name='ed').first()
# print session.dirty
# session.commit()
# print ed_user.id

# session.rollback()
# print ed_user.id
print dir(engine)
print dir(engine.drop)
print engine.table_names.__str__
print dir(engine.table_names.__str__)
