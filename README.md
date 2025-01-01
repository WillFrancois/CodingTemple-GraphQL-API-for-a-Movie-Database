# GraphQL API For A Movie Database

This project allows users to manipulate a MySQL database using GraphiQL to perform queries and mutations directly from their browser to their database.

## Database Set-up

To set up the database for this project to work, create a MySQL database on port 3306 with the password "CodingTemple" for the root user. After this, create a database named "movie_db".

## Python Environment Set-up

To create the Python environment needed for this code, run the command "python -m venv (your venv folder name here)" and use the virtual environment's pip to install the dependencies from the requirements.txt file.

## Running the Code

To run the code properly after installing the dependencies, use the flask binary available in your virtual environment's bin folder to deploy the server.

## Accessing the GraphiQL Dashboard

The GraphiQL dashboard is available from your web browser. Access the port your flask server is running on and add '/graphql' to start running commands.

### Queries:

- movies: Gives all movies available in the database.
- genres: Gives all genres available in the database.
- getMoviesByGenre: A function that takes a genreId as input and produces all movies with the same genre.
- getGenreByMovie: A function that takes a movieId as input and produces the related genre.

### Mutations:

- createMovies: Creates a movie and inserts it into the database.
- createGenre: Creates a genre and inserts it into the database.
- updateMovies: Updates a movie in the database from the given information.
- updateGenre: Updates a genre in the database from the given information.
- deleteMovies: Deletes a movie in the database from a given id number.
- deleteGenre: Deletes a genre in the database from a given id number.
