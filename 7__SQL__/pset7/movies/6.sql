SELECT AVG(ratings.rating) FROM movies, ratings
WHERE movies.year=2012 AND movies.id = ratings.movie_id;