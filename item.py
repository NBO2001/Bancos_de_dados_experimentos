
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


    def __str__(self) -> str:
        string = f"Id:\t{self.id}\nASIN:\t{self.asin}\n  title: {self.title}\n  group:{self.group}\n   salesrank:{self.salesrank}\n  "
        string += f"similar:{self.similar}\n categories: {len(self.categories) if self.categories != None else 0}\n   {self.categories}\n  "
        string += f"Reviews: total: {self.reviews[0]} downloaded: {self.reviews[1]} avg_rating: {self.reviews[2]}\n "

        if self.list_reviews:
            for rvw in self.list_reviews:
                string += f"  {str(rvw)}\n "

        string += f"\n"
        return string
