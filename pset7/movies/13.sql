SELECT DISTINCT
       p.name
  FROM stars s
 INNER JOIN people p
    ON s.person_id = p.id

 WHERE s.movie_id IN(SELECT s.movie_id
                       FROM people p

                       INNER JOIN stars s
                          ON s.person_id = P.id

                       WHERE p.birth = 1958 AND p.name = 'Kevin Bacon'
                    )
   AND p.name != 'Kevin Bacon'