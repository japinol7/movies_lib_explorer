select * from catalog_director order by id;
select * from catalog_movie order by id;
select * from catalog_actor order by id;

select * from catalog_movie_actors order by id;

-- 1364 movies
select count(*) from catalog_movie;

-- Empty catalog tables
-- delete from catalog_movie where id > 0;
-- delete from catalog_director where id > 0;

-- delete from catalog_actor where id > 0;
-- delete from catalog_movie_actors where id > 0;

-- select * from catalog_movie where director_id is null;
-- select id, last_name, length(last_name) from catalog_actor where length(last_name) < 2;
-- select id, [cast], length([cast]) from catalog_movie where length([cast]) > 245;

-- select title, count(title) as title_count from catalog_movie
--      group by title
--      having title_count > 1
--      order by title;

-- update main.catalog_movie set language = 'English' where country in ('US', 'UK');
-- [IMP] resources: Add and fix data.
--------------------
--------------------
select cm.id, cm.title, cm.year, cm.decade, cm.runtime,
       cm.director_id, cd.first_name director_fn, cd.last_name director_ln,
       cm.country, cm.title_original, cm.cast,
       cm.description, cm.language, cm.note, cm.production_company,
       cm.cinematography, cm.genres, cm.picture, cm.producer, cm.writer,
       cm.created, cm.updated
    from catalog_movie cm
    left join catalog_director cd on cm.director_id = cd.id
    order by cm.title, cm.year, cd.last_name;
--------------------
--------------------
