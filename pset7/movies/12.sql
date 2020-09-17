SELECT a.title
  FROM(
        SELECT m.id, m.title
          FROM people p

         INNER JOIN stars s
            ON s.person_id = p.id

         INNER JOIN movies m
            ON m.id = s.movie_id

         WHERE p.name = 'Johnny Depp'
        )a
 INNER JOIN(
          SELECT m.id, m.title
          FROM people p

         INNER JOIN stars s
            ON s.person_id = p.id

         INNER JOIN movies m
            ON m.id = s.movie_id

         WHERE p.name = 'Helena Bonham Carter'
         )b
     ON a.id = b.id

  UNION

 SELECT b.title
  FROM(
        SELECT m.id, m.title
          FROM people p

         INNER JOIN stars s
            ON s.person_id = p.id

         INNER JOIN movies m
            ON m.id = s.movie_id

         WHERE p.name = 'Johnny Depp'
        )a
 INNER JOIN(
          SELECT m.id, m.title
          FROM people p

         INNER JOIN stars s
            ON s.person_id = p.id

         INNER JOIN movies m
            ON m.id = s.movie_id

         WHERE p.name = 'Helena Bonham Carter'
         )b
    ON a.id = b.id;