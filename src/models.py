import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    bio = Column(String(250), nullable=False)
    posts = relationship("Post", back_populates="usuario")
    comentarios = relationship("Comentario", back_populates="usuario")
    likes = relationship("Like", back_populates="usuario")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    contenido = Column(String(250), nullable=False)
    imagen_url = Column(String(250), nullable=False)
    fecha = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="posts")
    comentarios = relationship("Comentario", back_populates="post")
    likes = relationship("Like", back_populates="post")

class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    contenido = Column(String(250), nullable=False)
    fecha = Column(TIMESTAMP)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="comentarios")
    post = relationship("Post", back_populates="comentarios")

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="likes")
    post = relationship("Post", back_populates="likes")

engine = create_engine('sqlite:///social_media.db')
Base.metadata.create_all(engine)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
