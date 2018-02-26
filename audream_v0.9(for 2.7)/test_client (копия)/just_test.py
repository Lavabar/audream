import os
path = os.getcwd()

file_list = os.listdir(path + "\\variants")
number_files = len(file_list)
print(file_list)
print(number_files)
