# *************************************************
# <Author: Ryan Marinelli>
# <Date: 8/17/2018>
# <Capstone Project: TomeRater allows users to read and rate books>
#
# *************************************************

#A User class that create a User Object
class User:
    def __init__(self, name, email):
        self.name = name # a string
        self.email = email # a string
        self.books = {}  #dictionary of book objects to the users rating of the book

    # Returns the email associated with this user
    def get_email(self):
        return self.email

    # Changes the email
    def change_email(self, address):
        self.email = address
        print("Email has been updated.")

    def __repr__(self):
        return "User {username}, email: {email}, books read: {count}".format(username=self.name, email=self.email, count=len(self.books))

    def __eq__(self, other_user):
        return self.email == other_user.email and self.name == other_user.name

    def read_book(self, book, rating="None"):
        self.books[book] = rating

    def get_average_rating(self):
        avg = 0
        total = 0
        for key, value in self.books.items():
            if value == 'None':
                value = 0
            total += value
        try:
            avg = total/len(self.books.keys())
        except ZeroDivisionError:
            avg = 0

        return avg

#A Book class that create a Book Object
class Book:
    def __init__(self, title, isbn):
        self.title = title # this is a string
        self.isbn = isbn # this is a number
        self.rating = [] #stores a list of ratings

    # gets the title
    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, newisbn):
        self.isbn = newisbn
        print("Isbn has been updated")

    def add_rating(self, rating):
        if rating == 'None':
            rating = -1
        if rating >= 0 and rating <=4:
            self.rating.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        total = 0;
        for rating in self.rating:
            total += rating
        return total / len(self.rating)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title} by an unknown author".format(title=self.title)

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater:
    def __init__(self):
        self.users = {} #this will map a users email to the cooresponding User obeject
        self.books = {} #this will map a Book object to the number of Users that have read it
        self.all_isbns = []

    def check_newisbn(self, isbn): #checks for a new isbn
        check_isbn = False
        if isbn in self.all_isbns:
            check_isbn = False
        else:
            check_isbn = True
        return(check_isbn)

    def store_isbn(self, isbn): #stores all of the isbns so we can determine if the isbn is new or not later
        new_isbn = False
        new_isbn = self.check_newisbn(isbn)
        if new_isbn == True:
            self.all_isbns.append(isbn)
        return(new_isbn)

    def create_book(self, title, isbn):
        check = False
        check = self.check_newisbn(isbn)
        if check == True:
            self.store_isbn(isbn)
            return Book(title, isbn)
        else:
            print("This ISBN already exists")

    def create_novel(self, title, author, isbn):
        check = False
        check = self.check_newisbn(isbn)
        if check == True:
            self.store_isbn(isbn)
            return Fiction(title, author, isbn)
        else:
            print("This ISBN already exists")


    def create_non_fiction(self, title, subject, level, isbn):
        check = False
        check = self.check_newisbn(isbn)
        if check == True:
            self.store_isbn(isbn)
            return Non_Fiction(title, subject, level, isbn)
        else:
            print("This ISBN already exists")

    def add_book_to_user(self, book, email, rating="None"):
        if email in self.users.keys():
            user = self.users[email]
            user.read_book(book, rating)
            book.add_rating(rating)
            if book in self.books.keys():
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {email}!").format(email = self.email)

    def add_user(self, name, email, user_books= ["None"]):
        user = User(name, email)
        if self.isvalidemail(email) == True:
            if user in self.users.values():
                print("User already exists: " + name)
            else:
                self.users[email] = user
                if len(user_books) > 1:
                    for book in user_books:
                        self.add_book_to_user(book, email)
        else:
            print("invalid email address: " + email )

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def get_most_read_book(self):
        maxvalue = 0
        maxbook = ''
        for book in self.books.keys():
            if self.books[book] > maxvalue:
                maxvalue = self.books[book]
                maxbook = book
        return maxbook

    def highest_rated_book(self):
        maxrating = 0
        maxbook = ''
        for book in self.books.keys():
            if book.get_average_rating() > maxrating:
                maxrating = book.get_average_rating()
                maxbook = book
        return maxbook

    def most_positive_user(self):
        maxrating = 0
        maxuser = ''
        for user in self.users.keys():
            userobj = self.users[user]
            if userobj.get_average_rating() > maxrating:
                maxrating = userobj.get_average_rating()
                maxuser = userobj
        return maxuser

    def isvalidemail(self, email):
        if email.find("@") > 0 and (email.find(".com") > 0 or email.find(".edu") > 0  or email.find(".org") > 0 ):
            return True
        else:
            return False
