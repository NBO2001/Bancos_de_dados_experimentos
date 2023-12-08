
import re

class Item:
    
    id:         int     = None
    asin:       str     = None
    title:      str     = None
    group:      str     = None
    salesrank:  str     = None
    similar:    tuple   = None
    categories: tuple   = None

    def __init__(self,) -> None:
        pass

    def __str__(self) -> str:
        string = f"Id:\t{self.id}\nASIN:\t{self.asin}\n  title: {self.title}\n"
        return string


path_file = "./downloads/sample"

contents = []

with open(path_file, "r") as f:

    new_item = None

    tmp_str = ""
    for line in f:

        # verify if is start of item

        id = re.findall(r'\b(?:Id):\s*([^\n]+)', line)

        if len(id) != 0:

            if new_item != None:
                contents.append(new_item)
           
            new_item = Item()
            new_item.id = id[0]

        if new_item != None:
            
            asin_pattern = r'\b(?:ASIN):\s*([^\n]+)'
            title_pattern = r'\b(?:title):\s*([^\n]+)'


            asin = re.findall(asin_pattern, line)
            title = re.findall(title_pattern, line)

            if ( len(asin) != 0):
                new_item.asin = asin[0]
            
            if ( len(title) != 0):
                new_item.title = title[0]
            

                
        # if len(line.strip()) != 0:
        #     tmp_str += line
        # else:
        #     contents.append(tmp_str)
        #     tmp_str = ""


for cont in contents:
    print(cont)
    
# print(contents[2])

# pattern = r'\b(?:Id|ASIN|title|group|salesrank|similar|categories):\s*([^\n]+)'
# pattern_two = r'|\b(?:categories):\s*(.*?)(?:reviews|$)'

# # Use re.findall para extrair as correspondências
# matches = re.findall(pattern, contents[2], re.DOTALL | re.IGNORECASE)

# # 
# # Display the extracted values
# print(matches)