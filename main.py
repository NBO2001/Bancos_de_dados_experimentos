from config import Config
from readfile import readFile
from item import Item

# Download files
conf = Config()

path_file = "./downloads/sample"

contents = []

             
# The idea is to be the function for inserting into the database.
def addDatabase(item: Item):
    contents.append(item)
    

readFile(filename=path_file, callback=addDatabase)

for i in range(10,15):
    print(contents[i])
