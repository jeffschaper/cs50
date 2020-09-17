SELECT m.title,
       m.year
  FROM movies m
 WHERE m.title like 'Harry Potter%'
 ORDER BY m.year;