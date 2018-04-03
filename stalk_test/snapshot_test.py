import os

# local_dirs = []
# local_files = []
# for rt, dirs, files in os.walk("/home/fiile"):
#     for d in dirs:
#         local_dirs.append(rt + "/" + d + "/")
#     for f in files:
#         local_files.append(f)
#
# print(local_dirs)
# print(local_files)

print(" \n".join(os.listdir("/home/fiile")))
