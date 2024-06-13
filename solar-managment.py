import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String, unique=True, nullable=False)
    Email = db.Column(db.String, unique=True, nullable=False)
    Password = db.Column(db.String, nullable=False)
    Credits = db.Column(db.Integer, default=0)

    reviews = relationship("Review", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    Description = db.Column(db.String)
    Price = db.Column(db.Float, nullable=False)
    Availability = db.Column(db.Boolean, default=True)

    reviews = relationship("Review", back_populates="product")

class Review(Base):
    __tablename__ = 'reviews'

    ReviewID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.String)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

def create_engine_and_session():
    engine = db.create_engine('sqlite:///solar_system.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def add_user(session):
    print("Adding a user...")
    try:
        username = input("Enter the username >>> ")
        email = input("Enter the email >>> ")
        password = input("Enter the password >>> ")
        credits = int(input("Enter the credits >>> "))
        user = User(Username=username, Email=email, Password=password, Credits=credits)
        session.add(user)
        session.commit()
        print("User Added!")
    except IntegrityError:
        session.rollback()
        print("Error: Username or email already exists. Please try again.")

def add_product(session):
    print("Adding a product...")
    name = input("Enter the product name >>> ")
    description = input("Enter the product description >>> ")
    price = float(input("Enter the product price >>> "))
    availability = input("Is the product available (yes/no)? >>> ").strip().lower() == 'yes'
    product = Product(Name=name, Description=description, Price=price, Availability=availability)
    session.add(product)
    session.commit()
    print("Product Added!")

def add_review(session):
    print("Adding a review...")
    try:
        user_id = int(input("Enter the user ID >>> "))
        product_id = int(input("Enter the product ID >>> "))
        rating = int(input("Enter the rating (1-5) >>> "))
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        comment = input("Enter the comment >>> ")
        review = Review(UserID=user_id, ProductID=product_id, Rating=rating, Comment=comment)
        session.add(review)
        session.commit()
        print("Review Added!")
    except ValueError as e:
        print(f"Error: {e}")
    except IntegrityError:
        session.rollback()
        print("Error: User ID or Product ID does not exist. Please try again.")

def lookup_user(session):
    print("Looking up a user...")
    username = input("Enter the username >>> ")
    user = session.query(User).filter_by(Username=username).first()
    if user:
        print(f"User found: {user}")
    else:
        print("User not found.")

def lookup_product(session):
    print("Looking up a product...")
    name = input("Enter the product name >>> ")
    product = session.query(Product).filter_by(Name=name).first()
    if product:
        print(f"Product found: {product}")
    else:
        print("Product not found.")

def main():
    session = create_engine_and_session()

    while True:
        print("\nMenu:")
        print("1. Add a user")
        print("2. Add a product")
        print("3. Add a review")
        print("4. Look up a user")
        print("5. Look up a product")
        print("6. Quit")
        choice = input("Enter your choice >>> ").strip()

        if choice == '1':
            add_user(session)
        elif choice == '2':
            add_product(session)
        elif choice == '3':
            add_review(session)
        elif choice == '4':
            lookup_user(session)
        elif choice == '5':
            lookup_product(session)
        elif choice == '6':
            print("Quitting Program")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    print("Program Terminated!")

if __name__ == "__main__":
    main()

