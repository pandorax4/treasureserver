import os

block_set = set([1, 2, 3, 555])
block_list = list(block_set)

str_set = ','.join(str(x) for x in block_set)

print(str_set)
command = "python viewagent.py " + str_set

result = os.popen(command).read()
print(result)
print("end")
