import ipdb
from models import Author, session

# Test setup
def test_author():
    # Add a new author
    new_author = Author(name="John Doe")
    session.add(new_author)
    session.commit()

    # Set a breakpoint to inspect the new_author object and database
    ipdb.set_trace()

    # Query the author from the database
    authors = session.query(Author).all()
    print(f"Authors in database: {[author.name for author in authors]}")

if __name__ == "__main__":
    print("Starting debug session...")
    test_author()
