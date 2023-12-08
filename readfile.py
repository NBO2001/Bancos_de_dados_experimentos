
import re

class Item:
    
    id:         int     = None
    asin:       str     = None
    title:      str     = None
    group:      str     = None
    salesrank:  str     = None
    similar:    tuple   = None
    categories: list   = None

    def __init__(self,) -> None:
        pass

    def __str__(self) -> str:
        string = f"Id:\t{self.id}\nASIN:\t{self.asin}\n  title: {self.title}\n  group:{self.group}\n   salesrank:{self.salesrank}\n  similar:{self.similar}\n categories: {len(self.categories) if self.categories != None else 0}\n   {self.categories}\n\n"
        return string


path_file = "./downloads/sample"

contents = []

with open(path_file, "r") as f:

    new_item = None

    for line in f:

        # verify if is start of item

        id = re.findall(r'\b(?:Id):\s*([^\n]+)', line)

        if len(id) != 0:

            if new_item != None:
                # Futuramente adicionar no banco de dados aqui!
                contents.append(new_item)
           
            new_item = Item()
            
            new_item.id = id[0]

        if new_item != None:
            
            asin_pattern = r'\b(?:ASIN):\s*([^\n]+)'
            title_pattern = r'\b(?:title):\s*([^\n]+)'
            group_pattern = r'\b(?:group):\s*([^\n]+)'
            salesrank_pattern = r'\b(?:salesrank):\s*([^\n]+)'
            similar_pattern = r'\b(?:similar):\s*([^\n]+)'
            categories_pattern = r'\b(?:categories):\s*([^\n]+)'


            asin = re.findall(asin_pattern, line)
            title = re.findall(title_pattern, line)

            group = re.findall(group_pattern, line)
            salesrank = re.findall(salesrank_pattern, line)
            similar = re.findall(similar_pattern, line)

            categories = re.findall(categories_pattern, line)

            if ( len(asin) != 0):
                new_item.asin = asin[0]
            
            if ( len(title) != 0):
                new_item.title = title[0]
            
            if len(group) != 0:
                new_item.group = group[0]
            
            if len(salesrank) != 0:
                new_item.salesrank = salesrank[0]

            if len(similar) != 0:
                new_item.similar = similar[0]
            
            if (len(categories) != 0):

                qnt = int(categories[0].strip())
                ctgs = []

                for _ in range(qnt):

                    ln = next(f,None)
                    ctgs.append(ln.strip())
                
                new_item.categories = ctgs
    if new_item != None:
        # Futuramente adicionar no banco de dados aqui!
        contents.append(new_item)

            # Quero ler duas linhas aqui e depois fazer um seek para depois dessa linhas

                
        # if len(line.strip()) != 0:
        #     tmp_str += line
        # else:
        #     contents.append(tmp_str)
        #     tmp_str = ""


for cont in contents:
    print(cont)
    
# print(contents[2])

# pattern = r'\b(?:|group|salesrank|similar|categories):\s*([^\n]+)'
# pattern_two = r'|\b(?:categories):\s*(.*?)(?:reviews|$)'

# # Use re.findall para extrair as correspondências
# matches = re.findall(pattern, contents[2], re.DOTALL | re.IGNORECASE)

# # 
# # Display the extracted values
# print(matches)