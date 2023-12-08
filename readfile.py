import re
from review import Review
from item import Item
from category import Category

def readFile(filename: str = None, callback: callable = None):
    if filename is None:
        raise ValueError("filename is None")

    with open(filename, "r") as f:
        new_item = None

        id_pattern = re.compile(r'\b(?:Id):\s*([^\n]+)')
        asin_pattern = re.compile(r'\b(?:ASIN):\s*([^\n]+)')
        title_pattern = re.compile(r'\b(?:title):\s*([^\n]+)')
        group_pattern = re.compile(r'\b(?:group):\s*([^\n]+)')
        salesrank_pattern = re.compile(r'\b(?:salesrank):\s*([^\n]+)')
        similar_pattern = re.compile(r'\b(?:similar):\s*([^\n]+)')
        categories_pattern = re.compile(r'\b(?:categories):\s*([^\n]+)')
        reviews_patterns = re.compile(r'\b(?:reviews):\s*([^\n]+)')

        for line in f:
            # Check for the start of an item
            id_match = id_pattern.findall(line)
            if id_match:
                if new_item is not None and callback is not None:
                    callback(new_item)
                new_item = Item()
                new_item.id = id_match[0]

            if new_item is None:
                continue

            asin_match = asin_pattern.findall(line)
            title_match = title_pattern.findall(line)
            group_match = group_pattern.findall(line)
            salesrank_match = salesrank_pattern.findall(line)
            similar_match = similar_pattern.findall(line)
            categories_match = categories_pattern.findall(line)
            reviews_match = reviews_patterns.findall(line)

            if asin_match:
                new_item.asin = asin_match[0]
            elif title_match:
                new_item.title = title_match[0]
            elif group_match:
                new_item.group = group_match[0]
            elif salesrank_match:
                new_item.salesrank = salesrank_match[0]
            elif similar_match:
                new_item.similar = similar_match[0]
            elif categories_match:
                qnt = int(categories_match[0].strip())
                ctgs = [next(f, None).strip() for _ in range(qnt)]

                list_categorys_raw = [ [ Category(raw_category=y) for y in x.split("|") if len(y) > 0] for x in ctgs]

                new_item.categories = list_categorys_raw
            elif reviews_match:
                rwv = reviews_match[0]
                total = int(re.findall(r'\b(?:total):\s*([^\s]+)', rwv)[0]) if 'total' in rwv else None
                downloaded = int(re.findall(r'\b(?:downloaded):\s*([^\s]+)', rwv)[0]) if 'downloaded' in rwv else None
                avg_rating = float(re.findall(r'\b(?:avg rating):\s*([^\s]+)', rwv)[0]) if 'avg rating' in rwv else None
                new_item.reviews = (total, downloaded, avg_rating)
                new_item.list_reviews = [Review(next(f, None)) for _ in range(downloaded)]

        if new_item is not None and callback is not None:
            callback(new_item)
