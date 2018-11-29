from app import db
# import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin




@login.user_loader
def load_user(zid):
    return Student.get_by_id(zid)


class Student(UserMixin):
    def __init__(self, _id, email, password, full_name, birthday, image=None, friends=None, program=None, courses=None, home_suburb=None, home_latitude=None, home_longitude=None):
        self._id = _id
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.full_name = full_name
        self.birthday = birthday
        # self._id = uuid.uuid4().hex if _id is None else _id
        self.image = image
        self.friends = friends
        self.program = program
        self.courses = courses
        self.home_suburb = home_suburb
        self.home_latitude = home_latitude
        self.home_longitude = home_longitude

    # def __repr__(self):
    #     return '<User {}, name: {}>'.format(self.zid, self.full_name)

    def get_id(self):
        return self._id

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)



    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_id(cls, _id):
        data = db["students"].find_one({"_id": _id})
        return cls(**data) if data else None


    @classmethod
    def get_by_email(cls, email):
        data = db["students"].find_one({"email": email})
        return cls(**data) if data else None

    # @property
    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password_hash,
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
    #
    # def save_to_mongo(self):
    #     db["students"].insert(self.json())








data = Student.get_by_email("z5195734@unsw.edu.au")

print(data.json())

# student = Student("z5195734", 'z5195734@unsw.edu.au', "12345", "Luke Wang", '1999-09-22')
# print(student)
# print(student.json())

# print(Student.get_by_id(_id="z5195734"))

