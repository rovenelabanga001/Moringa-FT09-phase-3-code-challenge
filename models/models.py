from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = "sqlite:///articles.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind = engine)
session = Session()

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer(), primary_key = True, autoincrement = True)
    name = Column( String(), nullable = False)

    articles = relationship('Article', backref = 'author')

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Name must be longer than 0 characters")

        self._name = name
        # session.add(self)
        # session.commit()


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name can not be changed after initialization")

    def magazines(self, session):
        return session.query(Magazine).join(Article).filter(Article.author_id == self.id).distinct().all()

    def articles(self, session):
        return session.query(Article).filter(Article.author_id == self.id).all()
    
    def __repr__(self):
        return f"<Author: {self.name}>"


class Magazine(Base):
    __tablename__ = 'magazines'

    id = Column(Integer(), primary_key = True)
    name = Column( String(), nullable = False)
    category = Column( String(), nullable = False)

    articles = relationship('Article', backref ='magazine')


    def __init__(self, name, category):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be between 2 and 16 characters")

        if not isinstance(category, str):
            raise TypeError("Category must be a string")

        if len(category) == 0 :
            raise ValueError("Category must be longer than 0 characters")

        self._name = name
        self._category = category

        # session.add(self)
        # session.commit()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")

        if len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be between 2 and 16 characters")

        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string")

        if len(value) == 0 :
            raise ValueError("Category must be longer than 0 characters")

        self._category = value

    def contributors(self, session):
        return session.query(Author).join(Article).filter(Article.magazine_id == self.id).distinct().all()

    def articles(self, session):
        return session.query(Author).filter(Article.magazine_id == self.id).all()

    def article_titles(self, session):
        articles = self.articles(session)
        return [article.title for article in articles] if articles else None

    def contributing_authors(self, session):
        authors = session.query(Author).join(Article).filter(Article.magazine_id == self.id).all()
        return [author for author in authors if len(author.articles (session)) > 2] or None
    def __repr__(self):
        return f"<Magazine: {self.name}, Category: {self.category}>"


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer(), primary_key = True, autoincrement =True)
    title = Column(String(), nullable = False)
    author_id = Column(Integer(), ForeignKey('authors.id', nullable = False))
    magazine_id = Column(Integer(), ForeignKey('magazines.id'), nullable = False)

    author = relationship("Author", backref = 'articles')
    magazine = relationship("Magazine", backref = 'articles')

    def __init__(self, author, magazine, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")

        if len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be between 5 and 50 characters")

        if not hasattr(author, 'id') or not hasattr(magazine, 'id'):
            raise ValueError("Both author and magazine must be valid instances with the id")

        self._title = title
        self.author_id = author.id
        self.magazine_id = magazine.id

        session.add(self)
        session.commit()

    @property
    def title(self):
        return self._title
    
    @property
    def author(self, session):
        return session.query(Author).filter(Author.id == self.author_id).first()

    @property
    def magazine(self, session):
        return session.query(Magazine).filter(Magazine.id == self.magazine_id).first()

    def __repr__(self):
        return f'<Article: {self.title}, Author: {self.author.name}, Magazine: {self.magazine.name} >'


Base.metadata.create_all(engine)
        