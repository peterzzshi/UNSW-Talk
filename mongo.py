import os
from itertools import groupby
from pymongo import MongoClient
from werkzeug.security import generate_password_hash


client = MongoClient('localhost', 27017)
db = client["UNSW-Talk"]

students = db["students"]
posts = db["posts"]

students_dir = "dataset-medium"


def read_student_information(zid):
    # returns information for one student
    details_filename = os.path.join(students_dir, zid, "student.txt")
    image_path = os.path.join(students_dir, zid, "img.jpg")

    with open(details_filename) as f:
        fields = [line.strip().split(':') for line in f]

    student_information = {}
    for field in fields:
        if field[0] == "friends" or field[0] == "courses":
            student_information[field[0]] = field[1].strip()[1:-2].split(', ')
        elif field[0] == "zid":
            student_information['_id'] = zid
        # elif field[0] == "password":
        #     student_information["password_hash"] = generate_password_hash(field[1].strip())
        else:
            student_information[field[0]] = field[1].strip()
    student_information['image'] = image_path
    # student_information['_id'] = zid
    return student_information


def read_student_posts(zid):
    # returns posts for one student
    foldername = os.path.join(students_dir, zid)
    filenames = sorted(list(filter(lambda x: x[0].isdigit(), os.listdir(foldername))))

    posts_filenames_groups = [list(g) for k, g in groupby(filenames, key=lambda x: x[0])]

    def to_tuple(name):
        """Extract all numbers from file as tuple (8,1,3) ... etc."""
        return tuple(map(int, name.split(".")[0].split("-")))

    # posts_information = {
    #     '_id': zid
    # }

    posts = []
    
    for posts_filenames in posts_filenames_groups:
        # sort the files in order of post, comment, replies
        posts_filenames.sort(key=to_tuple)
        last_file = posts_filenames[0]

        post = {}
        with open(os.path.join(students_dir, zid, last_file)) as f:
            for line in f:
                if ': ' in line:
                    index = line.index(":")
                    post[line[:index]] = line[index + 1:].strip()

        comments = []
        for i in range(1, len(posts_filenames)):
            length = len(to_tuple(posts_filenames[i]))

            if length == 2:
                comment = {}
                with open(os.path.join(students_dir, zid, posts_filenames[i])) as f:
                    for line in f:
                        if ': ' in line:
                            index = line.index(":")
                            comment[line[:index]] = line[index + 1:].strip()
                comment["replies"] = []
                comments.append(comment)
                # Whenever a file of length 2 appears, it means a new comment
                last_file = posts_filenames[i]

            if length == 3:
                reply = {}
                with open(os.path.join(students_dir, zid, posts_filenames[i])) as f:
                    for line in f:
                        if ': ' in line:
                            index = line.index(":")
                            reply[line[:index]] = line[index + 1:].strip()
                comments[-1]["replies"].append(reply)

        post["comments"] = comments
        posts.append(post)

    # posts_information["posts"] = posts

    return posts


students.remove({})
posts.remove({})

student_ids = os.listdir(students_dir)

# read the datasets and save the contents to mongodb 
for student_id in student_ids:
    if student_id[0] == "z":
        student_information = read_student_information(student_id)
        students.insert(student_information)

        student_posts = read_student_posts(student_id)
        for student_post in student_posts:
        	posts.insert(student_post)
        # posts.insert(student_posts)


client.close()