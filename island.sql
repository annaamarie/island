--- CREATE TABLES ---

-- Table: career_stage
CREATE TABLE career_stage (
    ch_career_stage_id INT PRIMARY KEY,
    ch_career_stage CHAR(30)
);

-- Table: career_trend
CREATE TABLE career_trend (
    ch_career_trend_id INT PRIMARY KEY,
    ch_career_trend CHAR(30)
);

-- Table: artist_metadata
CREATE TABLE artist_metadata (
    artist_id INT PRIMARY KEY,
    artist_name VARCHAR(255),
    country_code CHAR(10),
    hometown_city VARCHAR(255),
    current_city VARCHAR(255),
    is_inactive BOOL,
    image_url VARCHAR(500),
    latest_album_release_date DATE,
    ch_artist_rank INT,
    ch_artist_score FLOAT,
    ch_career_stage_id INT,
    ch_career_trend_id INT
);

-- Table: related_artists
CREATE TABLE related_artists (
    related_artist_id INT PRIMARY KEY,
    artist_id INT,
    related_artist_name VARCHAR(255),
    related_artist_rank INT,
    related_artist_cm_rank INT,
    country_code CHAR(10),
    related_artist_sp_followers BIGINT,
    related_artist_sp_popularity INT,
    genre_id INT
);

-- Table: social_media_ages
CREATE TABLE social_media_ages (
    some_age_id INT PRIMARY KEY,
    artist_id INT,
    platform_id INT,
    date DATE,
    age_group VARCHAR(30),
    gender CHAR(20),
    percentage FLOAT
);

-- Table: social_media_countries
CREATE TABLE social_media_countries (
    some_country_id INT PRIMARY KEY,
    artist_id INT,
    platform_id INT,
    date DATE,
    country_code CHAR(10),
    rank INT,
    followers BIGINT,
    percent FLOAT
);

-- Table: countries
CREATE TABLE countries (
    country_code CHAR(10) PRIMARY KEY,
    country_name VARCHAR(255),
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8)
);

-- Table: spotify_top_cities
CREATE TABLE spotify_top_cities (
    sp_top_city_id INT PRIMARY KEY,
    artist_id INT,
    city_id CHAR(20),
    rank INT,
    listeners BIGINT
);

-- Table: cities
CREATE TABLE cities (
    city_id CHAR(20) PRIMARY KEY,
    city_name VARCHAR(255),
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8)
);

-- Table: social_media_platforms
CREATE TABLE social_media_platforms (
    platform_id INT PRIMARY KEY,
    platform_name VARCHAR(50)
);

-- Table: charts_region_artist
CREATE TABLE charts_region_artist (
    chart_region_id INT PRIMARY KEY,
    artist_id INT,
    country_code CHAR(10)
);

-- Table: genres
CREATE TABLE genres (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(100)
);

-- Table: artist_genre
CREATE TABLE artist_genre (
    artist_id INT,
    genre_id INT,
    PRIMARY KEY (artist_id, genre_id)
);

-- Table: albums
CREATE TABLE albums (
    album_id INT PRIMARY KEY,
    album_name VARCHAR(255)
);

-- Table: tracks
CREATE TABLE tracks (
    track_id INT PRIMARY KEY,
    track_name VARCHAR(255),
    artist_id INT
);

-- Table: track_album
CREATE TABLE track_album (
    track_id INT,
    album_id INT,
    PRIMARY KEY (track_id, album_id)
);

-- Table: top_tracks
CREATE TABLE top_tracks (
    top_track_id INT PRIMARY KEY,
    track_id INT,
    track_rank INT,
    sg_popularity INT
);

-- Table: playlist_type
CREATE TABLE playlist_type (
    playlist_type_id INT PRIMARY KEY,
    playlist_type CHAR(30)
);

-- Table: playlist_metric_type
CREATE TABLE playlist_metric_type (
    playlist_metric_type_id INT PRIMARY KEY,
    playlist_metric_type CHAR(20)
);

-- Table: playlist
CREATE TABLE playlist (
    playlist_id INT PRIMARY KEY,
    artist_id INT,
    playlist_type_id INT,
    playlist_metric_type_id INT,
    playlist_value BIGINT
);

-- Table: spotify_timeseries
CREATE TABLE spotify_timeseries (
    sg_time_id INT PRIMARY KEY,
    artist_id INT,
    date DATE,
    sg_followers BIGINT,
    sg_monthly_listeners BIGINT,
    sg_popularity INT
);

-- Table: charts
CREATE TABLE charts (
    chart_id INT PRIMARY KEY,
    artist_id INT,
    total_charts INT,
    total_tracks INT,
    most_popular_track VARCHAR(255),
    highest_chart_rank INT
);

-- Table: social_media_metrics
CREATE TABLE social_media_metrics (
    some_metric_id INT PRIMARY KEY,
    artist_id INT,
    ig_followers BIGINT,
    tt_followers BIGINT,
    tt_likes BIGINT,
    tt_top_video_comments BIGINT,
    tt_top_video_views BIGINT,
    tt_track_posts BIGINT
);

-- Table: social_media_timeseries
CREATE TABLE social_media_timeseries (
    some_time_id INT PRIMARY KEY,
    artist_id INT,
    platform_id INT,
    date DATE,
    followers BIGINT,
    engagement_rate FLOAT
);

--- FOREIGN KEYS ---

-- Foreign Keys for artist_metadata
ALTER TABLE artist_metadata
ADD CONSTRAINT artist_metadata_country_code_fkey FOREIGN KEY (country_code) REFERENCES countries(country_code);

ALTER TABLE artist_metadata
ADD CONSTRAINT artist_metadata_ch_career_stage_fkey FOREIGN KEY (ch_career_stage_id) REFERENCES career_stage(ch_career_stage_id);

ALTER TABLE artist_metadata
ADD CONSTRAINT artist_metadata_ch_career_trend_fkey FOREIGN KEY (ch_career_trend_id) REFERENCES career_trend(ch_career_trend_id);

-- Foreign Keys for related_artists
ALTER TABLE related_artists
ADD CONSTRAINT related_artists_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id) ON DELETE CASCADE;

ALTER TABLE related_artists
ADD CONSTRAINT related_artists_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES genres(genre_id);

ALTER TABLE related_artists
ADD CONSTRAINT related_artists_country_code_fkey FOREIGN KEY (country_code) REFERENCES countries(country_code);

-- Foreign Keys for social_media_ages
ALTER TABLE social_media_ages
ADD CONSTRAINT social_media_ages_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

ALTER TABLE social_media_ages
ADD CONSTRAINT social_media_ages_platform_id_fkey FOREIGN KEY (platform_id) REFERENCES social_media_platforms(platform_id);

-- Foreign Keys for social_media_countries
ALTER TABLE social_media_countries
ADD CONSTRAINT social_media_countries_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

ALTER TABLE social_media_countries
ADD CONSTRAINT social_media_countries_platform_id_fkey FOREIGN KEY (platform_id) REFERENCES social_media_platforms(platform_id);

ALTER TABLE social_media_countries
ADD CONSTRAINT social_media_countries_country_code_fkey FOREIGN KEY (country_code) REFERENCES countries(country_code);

-- Foreign Keys for spotify_top_cities
ALTER TABLE spotify_top_cities
ADD CONSTRAINT spotify_top_cities_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

ALTER TABLE spotify_top_cities
ADD CONSTRAINT spotify_top_cities_city_id_fkey FOREIGN KEY (city_id) REFERENCES cities(city_id);

-- Foreign Keys for charts_region_artist
ALTER TABLE charts_region_artist
ADD CONSTRAINT charts_region_artist_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

ALTER TABLE charts_region_artist
ADD CONSTRAINT charts_region_artist_country_code_fkey FOREIGN KEY (country_code) REFERENCES countries(country_code);

-- Foreign Keys for artist_genre
ALTER TABLE artist_genre
ADD CONSTRAINT artist_genre_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

ALTER TABLE artist_genre
ADD CONSTRAINT artist_genre_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES genres(genre_id);

-- Foreign Keys for tracks
ALTER TABLE tracks
ADD CONSTRAINT tracks_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

-- Foreign Keys for top_tracks
ALTER TABLE top_tracks
ADD CONSTRAINT top_tracks_track_id_fkey FOREIGN KEY (track_id) REFERENCES tracks(track_id);

-- Foreign Keys for track_album
ALTER TABLE track_album
ADD CONSTRAINT track_album_track_id_fkey FOREIGN KEY (track_id) REFERENCES tracks(track_id);

ALTER TABLE track_album
ADD CONSTRAINT track_album_album_id_fkey FOREIGN KEY (album_id) REFERENCES albums(album_id);

-- Foreign Keys for playlist
ALTER TABLE playlist
ADD CONSTRAINT playlist_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

ALTER TABLE playlist
ADD CONSTRAINT playlist_playlist_type_id_fkey FOREIGN KEY (playlist_type_id) REFERENCES playlist_type(playlist_type_id);

ALTER TABLE playlist
ADD CONSTRAINT playlist_playlist_metric_type_id_fkey FOREIGN KEY (playlist_metric_type_id) REFERENCES playlist_metric_type(playlist_metric_type_id);

-- Foreign Keys for spotify_timeseries
ALTER TABLE spotify_timeseries
ADD CONSTRAINT spotify_timeseries_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

-- Foreign Keys for charts
ALTER TABLE charts
ADD CONSTRAINT charts_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

-- Foreign Keys for social_media_metrics
ALTER TABLE social_media_metrics
ADD CONSTRAINT social_media_metrics_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

-- Foreign Keys for social_media_timeseries
ALTER TABLE social_media_timeseries
ADD CONSTRAINT social_media_timeseries_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artist_metadata(artist_id);

ALTER TABLE social_media_timeseries
ADD CONSTRAINT social_media_timeseries_platform_id_fkey FOREIGN KEY (platform_id) REFERENCES social_media_platforms(platform_id);

--- INSERT DATA FROM CSV FILES ---

-- Insert into career_stage
COPY career_stage(ch_career_stage_id, ch_career_stage)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_ch_career_stage.csv'
DELIMITER ',' CSV HEADER;

-- Insert into career_trend
COPY career_trend(ch_career_trend_id, ch_career_trend)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_ch_career_trend.csv'
DELIMITER ',' CSV HEADER;

-- Insert into albums
COPY albums(album_id, album_name)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_albums.csv'
DELIMITER ',' CSV HEADER;

-- Insert into genres
COPY genres(genre_id, genre_name)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_genres.csv'
DELIMITER ',' CSV HEADER;

-- Insert into playlist_metric_type
COPY playlist_metric_type(playlist_metric_type_id, playlist_metric_type)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_playlist_metric_type.csv'
DELIMITER ',' CSV HEADER;

-- Insert into playlist_type
COPY playlist_type(playlist_type_id, playlist_type)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_playlist_type.csv'
DELIMITER ',' CSV HEADER;

-- Insert into cities
COPY cities(city_id, city_name, latitude, longitude)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_cities.csv'
DELIMITER ',' CSV HEADER;

-- Insert into countries
COPY countries(country_code, country_name, latitude, longitude)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_countries.csv'
DELIMITER ',' CSV HEADER;

-- Insert into artist_metadata
COPY artist_metadata(artist_id, artist_name, country_code, hometown_city, current_city, is_inactive, image_url, latest_album_release_date, ch_artist_rank, ch_artist_score, ch_career_stage_id, ch_career_trend_id)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_artist_metadata.csv'
DELIMITER ',' CSV HEADER;

-- Insert into playlist
COPY playlist(playlist_id, artist_id, playlist_type_id, playlist_metric_type_id, playlist_value)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_playlist.csv'
DELIMITER ',' CSV HEADER;

-- Insert into artist_genre
COPY artist_genre(artist_id, genre_id)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_artist_genre.csv'
DELIMITER ',' CSV HEADER;

-- Insert into charts
COPY charts(chart_id, artist_id, total_charts, total_tracks, most_popular_track, highest_chart_rank)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_charts.csv'
DELIMITER ',' CSV HEADER;

-- Insert into related_artists
COPY related_artists(related_artist_id, artist_id, related_artist_name, related_artist_rank, related_artist_cm_rank, country_code, related_artist_sp_followers, related_artist_sp_popularity, genre_id)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_related_artists.csv'
DELIMITER ',' CSV HEADER;

-- Insert into social_media_platforms
COPY social_media_platforms(platform_id, platform_name)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_social_media_platforms.csv'
DELIMITER ',' CSV HEADER;

-- Insert into social_media_metrics
COPY social_media_metrics(some_metric_id, artist_id, ig_followers, tt_followers, tt_likes, tt_top_video_comments, tt_top_video_views, tt_track_posts)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_social_media_metrics.csv'
DELIMITER ',' CSV HEADER;

-- Insert into social_media_ages
COPY social_media_ages(some_age_id, artist_id, platform_id, date, age_group, gender, percentage)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_social_media_ages.csv'
DELIMITER ',' CSV HEADER;

-- Insert into social_media_countries
COPY social_media_countries(some_country_id, artist_id, platform_id, date, country_code, rank, followers, percent)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_social_media_countries.csv'
DELIMITER ',' CSV HEADER;

-- Insert into social_media_timeseries
COPY social_media_timeseries(some_time_id, artist_id, platform_id, date, followers, engagement_rate)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_social_media_timeseries.csv'
DELIMITER ',' CSV HEADER;

-- Insert into spotify_timeseries
COPY spotify_timeseries(sg_time_id, artist_id, date, sg_followers, sg_monthly_listeners, sg_popularity)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_spotify_timeseries.csv'
DELIMITER ',' CSV HEADER;

-- Insert into spotify_top_cities
COPY spotify_top_cities(sp_top_city_id, artist_id, city_id, rank, listeners)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_spotify_top_cities.csv'
DELIMITER ',' CSV HEADER;

-- Insert into tracks
COPY tracks(track_id, track_name, artist_id)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_tracks.csv'
DELIMITER ',' CSV HEADER;

-- Insert into track_album
COPY track_album(track_id, album_id)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_track_album.csv'
DELIMITER ',' CSV HEADER;

-- Insert into top_tracks
COPY top_tracks(top_track_id, track_id, track_rank, sg_popularity)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_top_tracks.csv'
DELIMITER ',' CSV HEADER;

-- Insert into charts_region_artist
COPY charts_region_artist(chart_region_id, artist_id, country_code)
FROM '/Users/annawalter/Desktop/Final CSV Files/er_charts_region_artist.csv'
DELIMITER ',' CSV HEADER;