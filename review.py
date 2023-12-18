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

        helpful_pattern = r'\b(?:helpful):\s*([^\s]+)'

        helpful = re.findall(helpful_pattern, line)
        self.helpful = int(helpful[0]) if len(helpful) != 0 else None

    def __str__(self,):
        string = f"Date: {self.date}, Customer: {self.customer}, Rating: {self.rating}, "
        string += f"Votes: {self.votes}, Helpful: {self.votes}"

        return string

