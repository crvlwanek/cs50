SELECT DISTINCT(name) FROM stars
JOIN people ON stars.person_id = people.id
JOIN movies ON stars.movie_id = movies.id
WHERE name != "Kevin Bacon" AND title IN(
SELECT title FROM stars
JOIN people ON stars.person_id = people.id
JOIN movies ON stars.movie_id = movies.id
WHERE name = "Kevin Bacon" AND birth = 1958);