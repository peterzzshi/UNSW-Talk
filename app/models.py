from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(zid):
    return Student.get_by_id(zid)


class Student(UserMixin):
    def __init__(self, _id, email, password, full_name, birthday, image=None, friends=None, program=None, courses=None, home_suburb=None, home_latitude=None, home_longitude=None):
        self._id = _id
        self.email = email
        self.password = password
        # self.password_hash = generate_password_hash(password)
        self.full_name = full_name
        self.birthday = birthday
        self.image = image
        self.friends = friends
        self.program = program
        self.courses = courses
        self.home_suburb = home_suburb
        self.home_latitude = home_latitude
        self.home_longitude = home_longitude

    def __repr__(self):
        return '<User {}, name: {}>'.format(self._id, self.full_name)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_id(self):
        return self._id

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    def check_password(self, input_password):
        return self.password == input_password



    @classmethod
    def get_by_id(cls, _id):
        data = db["students"].find_one({"_id": _id})
        return cls(**data) if data else None

    @classmethod
    def get_by_email(cls, email):
        data = db["students"].find_one({"email": email})
        return cls(**data) if data else None

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            # "password_hash": self.password_hash,
            "full_name": self.full_name,
            "birthday": self.birthday,
            "image": self.image,
            "friends": self.friends,
            "program": self.program,
            "courses": self.courses,
            "home_suburb": self.home_suburb,
            "home_latitude": self.home_latitude,
            "home_longitude": self.home_longitude
        }

    def save_to_mongo(self):
        db["students"].insert(self.json())








# data = Student.get_by_email("z5195734@unsw.edu.au")
#
# print(data.json())

# student = Student("z5195731", 'z5195731@unsw.edu.au', 12345, "Luke Wang", '1999-09-22')
# print(student)
# student.save_to_mongo()
# print(student)

# print(Student.get_by_id(_id="z5195731"))

