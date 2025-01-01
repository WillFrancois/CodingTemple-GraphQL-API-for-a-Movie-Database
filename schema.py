import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db, Movie as MovieModel, Genre as GenreModel
from graphene import ObjectType, String, Schema, Boolean
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, text

class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel
        fields = ("genre_id")

class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

class CreateGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, name):
        with Session(db.engine) as session:
            with session.begin():
                if len(name) < 1:
                    genre = GenreModel(name="Error: Name is too short")
                    return CreateGenre(genre = genre)
                else:
                    genre = GenreModel(name=name)
                    session.add(genre)

            session.refresh(genre)
            return CreateGenre(genre=genre)

class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        name = graphene.String(required = True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id, name):
        with Session(db.engine) as session:
            with session.begin():
                exists = session.execute(select(GenreModel).where(GenreModel.id==id)).first()
                if exists:
                    genre = GenreModel(id=id, name=name)
                else:
                    genre = GenreModel(id=0, name="Error: ID does not exist")
                    return UpdateGenre(genre=genre)

            session.merge(genre)
            session.commit()
            return UpdateGenre(genre=genre)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                exists = session.execute(select(GenreModel).where(GenreModel.id==id)).first()
                if exists:
                    session.execute(delete(GenreModel).where(GenreModel.id==id))
                    ok = True
                else:
                    ok = False

            session.commit()
            return DeleteGenre(ok)


class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    genres = graphene.List(Genre)
    getMoviesByGenre = graphene.List(Movie, genre_id=graphene.Int())
    getGenreByMovie = graphene.Field(Genre, movie_id=graphene.Int())

    def resolve_movies(self, info):
        return db.session.execute(db.select(MovieModel)).scalars()

    def resolve_genres(self, info):
        return db.session.execute(db.select(GenreModel)).scalars()

    def resolve_getMoviesByGenre(self, info, genre_id):
        return db.session.execute(db.select(MovieModel).where(MovieModel.genre_id == genre_id)).scalars()

    def resolve_getGenreByMovie(self, info, movie_id):
        gen_id = db.session.execute(db.select(MovieModel.genre_id).where(MovieModel.id == movie_id)).first()[0]
        return db.session.execute(db.select(GenreModel).where(GenreModel.id == gen_id)).first()[0]

class Mutation(graphene.ObjectType):
    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()
