from readfile import readFile
from item import Item


path_file = "./downloads/sample"

contents = []

             
# The idea is to be the function for inserting into the database.
def addDatabase(item: Item):
    contents.append(item)
    

readFile(filename=path_file, callback=addDatabase)

for i in range(5,10):
    print(contents[i])