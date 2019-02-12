from sqlalchemy.orm import sessionmaker
from dataQueue import engine, User, config


Session = sessionmaker(bind=engine)
session = Session()
"""
# user = User()
# user.id = uid
# user.username = u_name
"""

uid = input("Enter the id : ")
u_id = '{}'.format(uid)
u_name = input("Enter username : ")
u_comment = input("Enter comment : ")


x = session.query(User).filter(User.id == u_id).first()
x.username = u_name
x.comment = u_comment
session.commit()
session.close()


"""
media = (id=123, title="Titular Line", slug="titular-line", type="movie")
media.update()

"""


"""
# session.query(user).filter(user.id == uid).update({'username': uname})
session.commit()

# session.query(user).update()
session.close()

"""
