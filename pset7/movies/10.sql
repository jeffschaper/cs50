SELECT p.name
  FROM(SELECT DISTINCT
              d.person_id
        FROM directors d
       INNER JOIN ratings r
          ON r.movie_id = d.movie_id

       WHERE r.rating >= 9.0
       )a

 INNER JOIN people p
    ON p.id = a.person_id;