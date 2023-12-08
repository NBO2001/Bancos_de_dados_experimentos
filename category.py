import re
class Category:
    category_id: int = None
    category_name: str = None


    def __init__(self, raw_category: str = None) -> None:

        
        pattern_category = r'([^[\]]+)'

        result = re.findall(pattern_category, raw_category)

        if len(result) != 0:
            
            if len(result) == 2:
                name, id = result
                id = int(id)

                self.category_id  = id
                self.category_name = name
            else:
                try:
                    self.category_id  = int(result[0])
                except:
                    self.category_name = result[0]
        
    def __str__(self) -> str:
        string = f"{self.category_name}[{self.category_id}]"
        return string

