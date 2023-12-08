
import re

class Review:

    customer: str = None
    date: str = None
    rating: int = 0
    votes: int = 0
    helpful: int = 0

    def __init__(self, initialLine: str = None) -> None:

        if initialLine:
            self.__process_line(initialLine)


    def __process_line(self, line):

        date_pattern = r'([0-9]+-[0-9]+-[0-9]+)'

        date = re.findall(date_pattern,  line)
        self.date = date[0] if len(date) != 0 else None

        customer_pattern = r'\b(?:cutomer):\s*([^\s]+)'

        customer = re.findall(customer_pattern, line)
        self.customer = customer[0] if len(customer) != 0 else None

        rating_pattern = r'\b(?:rating):\s*([^\s]+)'

        rating = re.findall(rating_pattern, line)
        self.rating = int(rating[0]) if len(rating) != 0 else None

        votes_pattern = r'\b(?:votes):\s*([^\s]+)'

        votes = re.findall(votes_pattern, line)
        self.votes = int(votes[0]) if len(votes) != 0 else None

        helpful_pattern = r'\b(?:votes):\s*([^\s]+)'

        helpful = re.findall(helpful_pattern, line)
        self.helpful = int(helpful[0]) if len(helpful) != 0 else None

    def __str__(self,):
        string = f"Date: {self.date}, Customer: {self.customer}, Rating: {self.rating}, "
        string += f"Votes: {self.votes}, Helpful: {self.votes}"

        return string


class Item:
    
    id:         int     = None
    asin:       str     = None
    title:      str     = None
    group:      str     = None
    salesrank:  str     = None
    similar:    tuple   = None
    categories: list    = None
    reviews:    tuple   = (None,None,None)  # (total, downloaded, avg_rating)
    list_reviews: list  = None  # list of the reviews


    def __init__(self,) -> None:
        pass

    def __str__(self) -> str:
        string = f"Id:\t{self.id}\nASIN:\t{self.asin}\n  title: {self.title}\n  group:{self.group}\n   salesrank:{self.salesrank}\n  "
        string += f"similar:{self.similar}\n categories: {len(self.categories) if self.categories != None else 0}\n   {self.categories}\n  "
        string += f"Reviews: total: {self.reviews[0]} downloaded: {self.reviews[1]} avg_rating: {self.reviews[2]}\n "

        if self.list_reviews:
            for rvw in self.list_reviews:
                string += f"  {str(rvw)}\n "

        string += f"\n"
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

            reviews_patterns = r'\b(?:reviews):\s*([^\n]+)'
            reviews = re.findall(reviews_patterns, line)
            
            if len(reviews) != 0:
                rwv = reviews[0]

                total = re.findall(r'\b(?:total):\s*([^\s]+)', rwv)
                downloaded = re.findall(r'\b(?:downloaded):\s*([^\s]+)', rwv)
                avg_rating = re.findall(r'\b(?:avg rating):\s*([^\s]+)', rwv)

                total       = int(total[0]) if len(total) != 0 else None
                downloaded  = int(downloaded[0]) if len(downloaded) != 0 else None
                avg_rating  = float(avg_rating[0]) if len(avg_rating) != 0 else None

                new_item.reviews = (total,downloaded, avg_rating)
                
                for _ in range(downloaded):

                    line = next(f, None)
                    customer = Review(line)
                    if new_item.list_reviews == None:
                        new_item.list_reviews = [] 

                    new_item.list_reviews.append(customer) 



    if new_item != None:
        # Futuramente adicionar no banco de dados aqui!
        contents.append(new_item)

            # Quero ler duas linhas aqui e depois fazer um seek para depois dessa linhas

                
        # if len(line.strip()) != 0:
        #     tmp_str += line
        # else:
        #     contents.append(tmp_str)
        #     tmp_str = ""


for i in range(5):
    print(contents[i])

# print(contents[2].list_reviews)

# for cont in contents:
#     print(cont)
    
# print(contents[2])

# pattern = r'\b(?:|group|salesrank|similar|categories):\s*([^\n]+)'
# pattern_two = r'|\b(?:categories):\s*(.*?)(?:reviews|$)'

# # Use re.findall para extrair as correspondências
# matches = re.findall(pattern, contents[2], re.DOTALL | re.IGNORECASE)

# # 
# # Display the extracted values
# print(matches)