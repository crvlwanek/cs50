SELECT people.name FROM people, directors, movies, ratings
WHERE people.id = directors.person_id
AND movies.id = directors.movie_id
AND movies.id = ratings.movie_id
AND ratings.rating >= 9.0;