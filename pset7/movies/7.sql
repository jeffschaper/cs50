SELECT m.title,
       r.rating
  FROM ratings r
 
 INNER JOIN movies m
    ON m.id = r.movie_id
 
 WHERE m.year = 2010
 
 ORDER BY r.rating DESC,
          m.title;