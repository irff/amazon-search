class Product:
    """
    A class representing an Amazon Product structure
    """
    YES = 'yes'
    NO = 'no'
    NONE = '-'

    def __init__(self, asin='-', image='-', link='-', price='-', prime=NO,
                 rating='-', reviews='-', sponsored=NO, title='-'):

        # Amazon Standard Identification Number (ASIN) is a 10 digit unique code
        # that identifies a product in Amazon
        self.asin = asin

        self.image = image
        self.link = link
        self.price = price
        self.prime = prime
        self.rating = rating
        self.reviews = reviews
        self.sponsored = sponsored
        self.title = title

    def to_dict(self):
        return self.__dict__

    def is_prime(self):
        return self.prime == self.YES

    def is_sponsored(self):
        return self.sponsored == self.YES
