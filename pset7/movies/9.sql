SELECT DISTINCT
       p.name
  FROM people p

INNER JOIN (SELECT DISTINCT s.person_id
              FROM stars s

             INNER JOIN movies m
                ON m.id = s.movie_id

             WHERE m.year = 2004
            )a
   ON a.person_id = p.id

ORDER BY p.birth;