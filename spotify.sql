create database spotify_db;

use spotify_db;
DROP TABLE IF EXISTS spotify_tracks;
CREATE TABLE spotify_tracks (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    track_name VARCHAR(255),  
    artist_name VARCHAR(255),  
    album_name VARCHAR(255),  
    release_date DATE,
    duration_minutes FLOAT,
    popularity INT
);

select * from spotify_tracks;

-- Most popular song
select track_name, artist_name, album_name, popularity
from spotify_tracks
order by popularity desc 
limit 1;

-- Average popularity
select  avg(popularity) as avg_popularity
from spotify_tracks;

-- songs have more than 4min duration
select track_name
from spotify_tracks 
where duration_minutes > 4.0;

-- popularity groups 
select 
	case 
		when popularity > 80 then 'High Popularity'
		when popularity > 50 then 'Medium Popularity'
		when popularity < 50 then 'low Popularity'
	end as popularity_range,
	count(*) track_count
from spotify_tracks
group by popularity_range
    


