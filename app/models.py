from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(zid):
    return Student.get_by_id(zid)


class Student(UserMixin):
    def __init__(self, _id, email, password, full_name, birthday, image=None, friends=[], program=None, courses=None, home_suburb=None, home_latitude=None, home_longitude=None):
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

    def friends_with(self, zid):
        return zid in self.friends

    def add_friend(self, zid):
        if self.friends_with(zid):
            return False
        else:
            self.friends.append(zid)
            new_friend = Student.get_by_id(zid)
            new_friend.friends.append(self._id)

            db["students"].update_one({"_id": self._id}, {"$set": self.json()})
            db["students"].update_one({"_id": new_friend._id}, {"$set": new_friend.json()})

    def remove_friend(self, zid):
        if self.friends_with(zid):
            self.friends.remove(zid)
            lost_friend = Student.get_by_id(zid)
            lost_friend.friends.remove(self._id)
            db["students"].update_one({"_id": self._id}, {"$set": self.json()})
            db["students"].update_one({"_id": lost_friend._id}, {"$set": lost_friend.json()})
        else:
            return False


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


class Post():
    def __init__(self, author, message, ):


        post = {"_id": "z5198807", "posts": [{"latitude": "-33.9104", "from": "z5198807",
                                       "message": "To the Middle Eastern (Indian?) invigilator in my Chem1011 midexam at Clancy auditorium today, I think I failed my test. I can't stop looking at your handsome face and hot chest. Your butt is really nice too in those black jeans. (I'm not a lady. Sorry if I got you excited for the first few lines there.) Still! XOXOXOX",
                                       "longitude": "151.2316", "time": "2013-05-10T05:39:28+0000", "comments": []}, {
                                          "message": "To that girl who seems a bit crazy who's in my math1041 tutorials friday 1pm. Others may think ur ape shit crazy and all... But i think ur amazing and i find your shennigans seductive ... tell me to shut up more please... it gets my calculator to rise exponentially. From your secret admirier",
                                          "longitude": "151.2219", "from": "z5198807",
                                          "time": "2013-05-10T07:37:38+0000", "latitude": "-33.9200", "comments": [
                {"from": "z5197178", "time": "2013-05-10T05:37:52+0000", "message": "z5194082", "replies": []},
                {"message": "z5197178 Ain't even me", "time": "2013-05-10T07:37:38+0000", "from": "z5194082",
                 "replies": []}]}, {"time": "2016-04-28T05:03:45+0000", "latitude": "-33.7492",
                                    "message": "Where to meet new people (especially girls without them getting all defensive) UNSW?",
                                    "from": "z5198807", "longitude": "151.1093", "comments": [
                {"time": "2016-04-27T12:04:25+0000",
                 "message": "Need to be on campus, first of all. Go around campus and apply or join something that a lot of girls take part in (you figure that out).",
                 "from": "z5190454", "replies": []}, {
                    "message": "Considering a change in degrees? With a 50/50 ratio you'll never be disappointed in Biomedical Engineering!",
                    "from": "z5196684", "time": "2016-04-27T13:27:06+0000",
                    "replies": [{"message": "can confirm", "from": "z5197178", "time": "2016-04-27T13:28:07+0000"}]},
                {"from": "z5190129", "message": "Join Arc Yellow Shirts, guarantee 100 girls on the beach",
                 "time": "2016-04-27T09:52:59+0000", "replies": []},
                {"time": "2016-04-27T09:00:27+0000", "message": "You don't", "from": "z5190009", "replies": []},
                {"message": "cofa", "from": "z5196487", "time": "2016-04-27T14:06:05+0000", "replies": []},
                {"message": "z5191824 is this u", "time": "2016-04-27T09:06:18+0000", "from": "z5194082",
                 "replies": [{"from": "z5191824", "message": "I pull tho", "time": "2016-04-27T09:07:13+0000"},
                             {"time": "2016-04-27T09:07:31+0000", "from": "z5194082",
                              "message": "ha ha ha ur hilarious xd"}]},
                {"message": "z5194685", "from": "z5193757", "time": "2016-04-28T05:03:45+0000", "replies": []}]},
                                      {"time": "2016-05-02T08:17:48+0000", "from": "z5198807", "latitude": "-33.8727",
                                       "longitude": "151.1402",
                                       "message": "Saroop Philip, I swear imma hunt 'her moistness' down and dump her in Calcium Chloride Desiccant so that her existence will disappear with her moist self. Ain't no hoe gonna steal you from me, lets face it you need me to integrate your natural log which she can't handle.\\n\\nFrom,\\nYour one and only Lover <3",
                                       "comments": [{"from": "z5190995",
                                                     "message": "z5197178 get ready for the roast of your life",
                                                     "time": "2016-04-29T08:39:08+0000", "replies": []}, {
                                                        "message": "z5196684 is this the same person.... From primary? 😂😂😂😂😂😂",
                                                        "from": "z5193757", "time": "2016-05-02T06:38:49+0000",
                                                        "replies": []},
                                                    {"message": "z5195369 z5191824 Andrew z5190129   z5198491 z5194082",
                                                     "time": "2016-04-29T08:19:15+0000", "from": "z5198491",
                                                     "replies": []},
                                                    {"from": "z5193757", "time": "2016-05-02T06:39:10+0000",
                                                     "message": "z5191841 is this..... 😂😂😂😂😂😂", "replies": [
                                                        {"message": "Wtf? I know him", "from": "z5191841",
                                                         "time": "2016-05-02T08:17:48+0000"}]},
                                                    {"time": "2016-04-29T08:16:57+0000", "from": "z5194685",
                                                     "message": "z5197178", "replies": []}]}, {
                                          "message": "Yesterday (4th May) around 6:07 PM, i was passing around the UNSW gym finishing my workout, and the way between gym and Mamak village i saw two Asian girls passing through. And at the moment i saw her face, my feet just stopped and i had to look back again. Now my most regretful time in my whole life is, I didn't run back and ask for her name. I really want to see her again. Please help me people",
                                          "latitude": "-33.9050", "time": "2016-05-16T11:46:11+0000",
                                          "longitude": "151.1564", "from": "z5198807", "comments": []}, {
                                          "message": "I still remember the first time I saw you, you walked into my FINS2624 - Portfolio Management lecture... that body of yours, so beautifully distributed...and that tail, so risk-é! Your a real asset to the course and I can only imagine how you would send my sharpe ratio through the roof. I know this might sound irrational, but who knows, maybe one day I'll random walk you down the aisle and turn this bond of ours into a perpetuity. I know I'm probably coming across a little strong, but I hope you take this at face value and don't discount my interest.\\n\\nSee you in the futures x",
                                          "latitude": "-33.7416", "longitude": "150.8499",
                                          "time": "2016-05-16T21:44:00+0000", "from": "z5198807", "comments": [
                    {"from": "z5194685", "time": "2016-05-16T21:44:00+0000", "message": "z5194082 z5197178",
                     "replies": []}]}, {"from": "z5198807", "longitude": "151.0459", "latitude": "-33.9009",
                                        "time": "2016-05-31T15:17:21+0000",
                                        "message": "Jason K I've been talking to you for a few weeks and have been observing you in physics lectures. I pretend to be bad at physics so that I can ask you for help ;) bae HSP and chill sometime?",
                                        "comments": [{"from": "z5190129",
                                                      "message": "z5194082 why you going to physics lectures",
                                                      "time": "2016-05-31T15:14:30+0000", "replies": [
                                                {"from": "z5194082", "time": "2016-05-31T15:16:30+0000",
                                                 "message": "Lol is not me haha"},
                                                {"message": "Do u think i will go to lectures 😂😂", "from": "z5194082",
                                                 "time": "2016-05-31T15:17:21+0000"}]},
                                                     {"time": "2016-05-30T23:52:19+0000", "from": "z5197178",
                                                      "message": "z5194685 - pulling from my uni also ? Haha",
                                                      "replies": []},
                                                     {"message": "z5193755 since when you go to my uni",
                                                      "time": "2016-05-30T13:43:19+0000", "from": "z5191841",
                                                      "replies": [{"time": "2016-05-30T13:43:50+0000", "message": "wtf",
                                                                   "from": "z5193755"}]},
                                                     {"from": "z5190520", "time": "2016-05-30T15:21:08+0000",
                                                      "message": "z5194685 why didnt u tell me u were at unsw bro",
                                                      "replies": []}, {"message": "z5193757 obviously you mate",
                                                                       "time": "2016-05-30T14:03:48+0000",
                                                                       "from": "z5196487", "replies": [
                                                    {"from": "z5193757", "message": "Last name is \"brah\" mate",
                                                     "time": "2016-05-30T14:06:52+0000"},
                                                    {"time": "2016-05-30T14:12:43+0000",
                                                     "message": "Alright kurusumuthu", "from": "z5196487"}]},
                                                     {"from": "z5195151", "message": "z5196487 You do physics?",
                                                      "time": "2016-05-30T23:34:24+0000", "replies": []},
                                                     {"time": "2016-05-30T14:33:19+0000", "from": "z5191824",
                                                      "message": "z5198807 didnt know you been sneaking in",
                                                      "replies": [{
                                                                      "message": "You could say he always gravitated to those lecture halls. Just couldn't get enough",
                                                                      "from": "z5191841",
                                                                      "time": "2016-05-31T00:42:13+0000"},
                                                                  {"from": "z5191824", "message": "BOOO^",
                                                                   "time": "2016-05-31T08:34:24+0000"}]},
                                                     {"message": "z5193757 this is you", "from": "z5196684",
                                                      "time": "2016-05-30T15:47:07+0000", "replies": []},
                                                     {"from": "z5191520", "time": "2016-05-30T13:04:50+0000",
                                                      "message": "z5193757 lmfaoooooo", "replies": [{
                                                                                                        "message": "as you can see, my last names actually \"brah\" and havnt been in a phys lecture in 4 yrs, dis not me mayn",
                                                                                                        "from": "z5193757",
                                                                                                        "time": "2016-05-30T13:09:09+0000"},
                                                                                                    {
                                                                                                        "message": "Kurusmoooorthy pls",
                                                                                                        "time": "2016-05-30T13:09:35+0000",
                                                                                                        "from": "z5191520"}]},
                                                     {
                                                         "message": "z5196487 z5190454 z5191125 z5195995 z5195928 z5190009",
                                                         "time": "2016-05-30T15:37:02+0000", "from": "z5193989",
                                                         "replies": []},
                                                     {"time": "2016-05-30T13:52:01+0000", "from": "z5190995",
                                                      "message": "z5190520 z5193757 z5197361 finally", "replies": [
                                                         {"from": "z5190520", "time": "2016-05-30T13:57:06+0000",
                                                          "message": "AHAHAHAHAHA"},
                                                         {"time": "2016-05-30T13:57:16+0000", "from": "z5190520",
                                                          "message": "Was this you z5192543???"},
                                                         {"from": "z5192543", "message": "yeh 100%",
                                                          "time": "2016-05-30T21:28:33+0000"},
                                                         {"from": "z5193757", "time": "2016-05-30T23:30:17+0000",
                                                          "message": "😂😂"},
                                                         {"message": "well this is fantastic!", "from": "z5190995",
                                                          "time": "2016-05-30T23:49:36+0000"}]},
                                                     {"message": "z5198807", "from": "z5195369",
                                                      "time": "2016-05-30T13:37:55+0000", "replies": [
                                                         {"message": "Was just about to tag him hahaha",
                                                          "time": "2016-05-30T13:55:03+0000", "from": "z5194476"},
                                                         {"time": "2016-05-30T14:25:07+0000",
                                                          "message": "lol only 2 years late hahah",
                                                          "from": "z5198807"}]},
                                                     {"from": "z5190688", "time": "2016-05-30T13:52:00+0000",
                                                      "message": "z5190995 z5190520 z5197361", "replies": [
                                                         {"message": "Hehehehehe", "from": "z5190520",
                                                          "time": "2016-05-30T13:57:21+0000"}]},
                                                     {"message": "z5191238", "time": "2016-05-30T23:50:08+0000",
                                                      "from": "z5195935", "replies": [
                                                         {"message": "😉", "time": "2016-05-30T23:51:07+0000",
                                                          "from": "z5191238"}]},
                                                     {"from": "z5198491", "time": "2016-05-30T22:33:05+0000",
                                                      "message": "z5198807 z5196487", "replies": []},
                                                     {"time": "2016-05-30T14:19:59+0000", "from": "z5199781",
                                                      "message": "z5194082", "replies": [
                                                         {"message": "Lol what is this haha", "from": "z5194082",
                                                          "time": "2016-05-30T19:37:29+0000"}]},
                                                     {"from": "z5190129", "time": "2016-05-30T22:23:33+0000",
                                                      "message": "z5193757", "replies": []},
                                                     {"message": "z5196487", "from": "z5191238",
                                                      "time": "2016-05-30T14:38:50+0000", "replies": [
                                                         {"time": "2016-05-30T15:10:33+0000", "from": "z5196487",
                                                          "message": "Yeah cause I transferred to Engo brah"}]},
                                                     {"from": "z5198757", "message": "z5199585",
                                                      "time": "2016-05-30T20:52:41+0000", "replies": [
                                                         {"from": "z5199585",
                                                          "message": "Don't do physics :( Also don't talk to people lol",
                                                          "time": "2016-05-31T00:43:55+0000"},
                                                         {"from": "z5198757", "time": "2016-05-31T01:48:20+0000",
                                                          "message": "That's why she pretends to be bad at it...it all adds up"}]},
                                                     {"message": "z5198410", "time": "2016-05-30T15:24:49+0000",
                                                      "from": "z5199953", "replies": []},
                                                     {"message": "z5190995", "time": "2016-05-30T13:51:39+0000",
                                                      "from": "z5190995", "replies": [
                                                         {"time": "2016-05-30T23:49:51+0000", "from": "z5190995",
                                                          "message": "yay"}]},
                                                     {"from": "z5192930", "message": "z5191405",
                                                      "time": "2016-05-31T04:43:25+0000", "replies": []},
                                                     {"message": "z5190995", "time": "2016-05-31T00:08:49+0000",
                                                      "from": "z5197433", "replies": []}]},
                                      {"time": "2016-06-28T14:26:41+0000", "from": "z5198807",
                                       "message": "JDate, anyone?", "latitude": "-33.7492", "longitude": "151.1093",
                                       "comments": []}]}

# Student("z5195731", 'z5195731@unsw.edu.au', 12345, "Luke Wang", '1999-09-22').save_to_mongo()


# print(Student.get_by_id("z5195731").friends)
