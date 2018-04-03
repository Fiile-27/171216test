from aip import AipFace

APP_ID = "11025440"
API_KEY = "GshnkrgbfFgUY9wbcjj6ZQYC"
SECRET_KEY = "06MBTnml2eIA4gZ5GpqiGflLRddvNkgd"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(file_path):
    with open(file_path, "rb") as fp:
        return fp.read()


images = [
    get_file_content("/home/fiile/Pictures/me.jpg"),
    get_file_content("/home/fiile/Pictures/me2.jpg"),
]

# print(client.detect(image))
print(client.match(images))

# options = {}
# options["max_face_num"] = 2
# options["face_fields"] = "age,beauty,expression,faceshape,gender,glasses,race,qualities"
#
# print(client.detect(image, options))
