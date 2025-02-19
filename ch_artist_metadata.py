import pandas as pd
import json
import glob

desired_fields = [
    # General
    "obj.id", # chartmetric artist id
    "obj.name", # artist name
    "obj.code2", # country code
    "obj.hometown_city", # hometown city
    "obj.current_city", # current city
    "obj.cm_artist_rank", # chartmetric artist rank
    "obj.cm_artist_score", # chartmetric artist score
    "obj.image_url",
    "obj.inactive", # binary indicator if artist is inactive
    "obj.cm_statistics.latest.latest_album_release_date", # latest album release date
    # Genres
    "obj.genres.primary.name", # primary genre
    "obj.genres.secondary[0].name", # sub genre 1
    "obj.genres.secondary[1].name", # sub genre 2
    "obj.cm_statistics.genreRank.rank", # genre rank for primary genre
    "obj.cm_statistics.secondaryGenreRanks[0].rank", # genre score for sub genre 1
    "obj.cm_statistics.secondaryGenreRanks[1].rank", # genre score for sub genre 2
    # Career
    "obj.career_status.stage", # career status stage
    "obj.career_status.stage_score", # career status stage score
    "obj.career_status.trend", # career status trend
    "obj.career_status.trend_score", # career status trend score
    # Spotify Top Cities
    "obj.cm_statistics.sp_where_people_listen[0].name", # top city
    "obj.cm_statistics.sp_where_people_listen[0].listeners", # top city listeners
    "obj.cm_statistics.sp_where_people_listen[1].name", # second top city
    "obj.cm_statistics.sp_where_people_listen[1].listeners", # second top city listeners
    "obj.cm_statistics.sp_where_people_listen[2].name", # third top city
    "obj.cm_statistics.sp_where_people_listen[2].listeners", # third top city listeners
    "obj.cm_statistics.sp_where_people_listen[3].name", # fourth top city
    "obj.cm_statistics.sp_where_people_listen[3].listeners", # fourth top city listeners
    "obj.cm_statistics.sp_where_people_listen[4].name", # fifth top city
    "obj.cm_statistics.sp_where_people_listen[4].listeners", # fifth top city listeners
    # Instagram Stats
    "obj.cm_statistics.latest.ins_engagement_rate", # instagram engagement rate
    "obj.cm_statistics.latest.ins_followers", # instagram followers
    "obj.cm_statistics.weekly_diff.ins_followers", # instagram followers difference to last week
    "obj.cm_statistics.monthly_diff.ins_followers", # instagram followers difference to last month
    # Spotify Stats
    "obj.cm_statistics.latest.sp_followers", # spotify followers
    "obj.cm_statistics.weekly_diff.sp_followers", # spotify followers difference to last week
    "obj.cm_statistics.monthly_diff.sp_followers", # spotify followers difference to last month
    "obj.cm_statistics.latest.sp_followers_to_listeners_ratio", # spotify followers to listeners ratio
    "obj.cm_statistics.latest.sp_listeners_to_followers_ratio", # spotify listeners to followers ratio
    "obj.cm_statistics.latest.sp_monthly_listeners", # spotify monthly listeners
    "obj.cm_statistics.weekly_diff.sp_monthly_listeners", # spotify monthly listeners difference to last week
    "obj.cm_statistics.monthly_diff.sp_monthly_listeners", # spotify monthly listeners difference to last month
    "obj.cm_statistics.latest.sp_popularity", # spotify popularity
    "obj.cm_statistics.weekly_diff.sp_popularity", # spotify popularity difference to last week
    "obj.cm_statistics.monthly_diff.sp_popularity", # spotify popularity difference to last month 
    "obj.cm_statistics.latest.spotify_ed_playlist_count", # spotify editorial playlist count
    "obj.cm_statistics.weekly_diff.num_sp_editorial_playlists", # spotify editorial playlist count difference to last week
    "obj.cm_statistics.monthly_diff.num_sp_editorial_playlists", # spotify editorial playlist count difference to last month
    "obj.cm_statistics.latest.spotify_ed_playlist_total_reach", # spotify editorial playlist total reach
    "obj.cm_statistics.weekly_diff.sp_editorial_playlist_total_reach", # spotify editorial playlist total reach difference to last week
    "obj.cm_statistics.monthly_diff.sp_editorial_playlist_total_reach", # spotify editorial playlist total reach difference to last month
    "obj.cm_statistics.latest.spotify_playlist_count", # spotify playlist count
    "obj.cm_statistics.weekly_diff.num_sp_playlists", # spotify playlist count difference to last week
    "obj.cm_statistics.monthly_diff.num_sp_playlists", # spotify playlist count difference to last month
    "obj.cm_statistics.latest.spotify_playlist_total_reach", # spotify playlist total reach
    "obj.cm_statistics.weekly_diff.sp_playlist_total_reach", # spotify playlist total reach difference to last week
    "obj.cm_statistics.monthly_diff.sp_playlist_total_reach", # spotify playlist total reach difference to last month
    "obj.cm_statistics.latest.spotify_popular_playlist_count", # spotify popular playlist count
    "obj.cm_statistics.latest.spotify_popular_playlist_total_reach", # spotify popular playlist total reach
    "obj.cm_statistics.latest.spotify_popular_playlist_tracks", # spotify popular playlist tracks
    # TikTok Stats
    "obj.cm_statistics.tiktok_followers", # tiktok followers
    "obj.cm_statistics.weekly_diff.tiktok_followers", # tiktok followers difference to last week
    "obj.cm_statistics.monthly_diff.tiktok_followers", # tiktok followers difference to last month
    "obj.cm_statistics.tiktok_likes", # tiktok likes
    "obj.cm_statistics.weekly_diff.tiktok_likes", # tiktok likes difference to last week
    "obj.cm_statistics.monthly_diff.tiktok_likes", # tiktok likes difference to last month
    "obj.cm_statistics.latest.tiktok_top_video_comments", # tiktok top video comments
    "obj.cm_statistics.weekly_diff.tiktok_top_video_comments", # tiktok top video comments difference to last week
    "obj.cm_statistics.monthly_diff.tiktok_top_video_comments", # tiktok top video comments difference to last month
    "obj.cm_statistics.latest.tiktok_top_video_views", # tiktok top video views
    "obj.cm_statistics.weekly_diff.tiktok_top_video_views", # tiktok top video views difference to last week
    "obj.cm_statistics.monthly_diff.tiktok_top_video_views", # tiktok top video views difference to last month
    "obj.cm_statistics.latest.tiktok_track_posts", # tiktok track posts
    "obj.cm_statistics.weekly_diff.tiktok_track_posts", # tiktok track posts difference to last week
    "obj.cm_statistics.monthly_diff.tiktok_track_posts", # tiktok track posts difference to last month
]

# Function to extract data for desired fields
def extract_data(json_data, fields):
    extracted = {}
    for field in fields:
        keys = field.split('.')
        value = json_data
        try:
            for key in keys:
                if '[' in key and ']' in key:  # Handle list indexing
                    key, index = key[:-1].split('[')
                    value = value[key][int(index)]
                else:
                    value = value[key]
            extracted[field] = value
        except (KeyError, IndexError, TypeError):  # Handle missing or malformed data
            extracted[field] = None
    return extracted

# Path to JSON files
json_files = glob.glob("/Users/annawalter/Library/Mobile Documents/com~apple~CloudDocs/Documents/Studium/Master/Data Science/3. Semester/BDBI/Exam BDBI/ch_artist_metadata/*.json")

# Read and process each JSON file
data = []
for file in json_files:
    with open(file, 'r') as f:
        json_data = json.load(f)
        data.append(extract_data(json_data, desired_fields))

# Convert to DataFrame
df = pd.DataFrame(data)

# Rename columns
df.rename(columns={
    # General
    'obj.id': 'ch_artist_id',
    'obj.name': 'artist_name',
    'obj.code2': 'country_code',
    'obj.hometown_city': 'hometown_city',
    'obj.current_city': 'current_city',
    'obj.cm_artist_rank': 'ch_artist_rank',
    'obj.cm_artist_score': 'ch_artist_score',
    'obj.image_url': 'image_url',
    'obj.inactive': 'is_inactive',
    'obj.cm_statistics.latest.latest_album_release_date': 'latest_album_release_date',

    # Genres
    'obj.genres.primary.name': 'primary_genre',
    'obj.genres.secondary[0].name': 'sub_genre_1',
    'obj.genres.secondary[1].name': 'sub_genre_2',
    'obj.cm_statistics.genreRank.rank': 'ch_primary_genre_rank',
    'obj.cm_statistics.secondaryGenreRanks[0].rank': 'ch_sub_genre_1_rank',
    'obj.cm_statistics.secondaryGenreRanks[1].rank': 'ch_sub_genre_2_rank',

    # Career
    'obj.career_status.stage': 'ch_career_stage',
    'obj.career_status.stage_score': 'ch_career_stage_score',
    'obj.career_status.trend': 'ch_career_trend',
    'obj.career_status.trend_score': 'ch_career_trend_score',

    # Spotify Top Cities
    'obj.cm_statistics.sp_where_people_listen[0].name': 'sp_top_city',
    'obj.cm_statistics.sp_where_people_listen[0].listeners': 'sp_top_city_listeners',
    'obj.cm_statistics.sp_where_people_listen[1].name': 'sp_second_top_city',
    'obj.cm_statistics.sp_where_people_listen[1].listeners': 'sp_second_top_city_listeners',
    'obj.cm_statistics.sp_where_people_listen[2].name': 'sp_third_top_city',
    'obj.cm_statistics.sp_where_people_listen[2].listeners': 'sp_third_top_city_listeners',
    'obj.cm_statistics.sp_where_people_listen[3].name': 'sp_fourth_top_city',
    'obj.cm_statistics.sp_where_people_listen[3].listeners': 'sp_fourth_top_city_listeners',
    'obj.cm_statistics.sp_where_people_listen[4].name': 'sp_fifth_top_city',
    'obj.cm_statistics.sp_where_people_listen[4].listeners': 'sp_fifth_top_city_listeners',

    # Instagram Stats
    'obj.cm_statistics.latest.ins_engagement_rate': 'ig_eng_rate',
    'obj.cm_statistics.latest.ins_followers': 'ig_followers',
    'obj.cm_statistics.weekly_diff.ins_followers': 'ig_followers_diff_weekly',
    'obj.cm_statistics.monthly_diff.ins_followers': 'ig_followers_diff_monthly',

    # Spotify Stats
    'obj.cm_statistics.latest.sp_followers': 'sp_followers',
    'obj.cm_statistics.weekly_diff.sp_followers': 'sp_followers_diff_weekly',
    'obj.cm_statistics.monthly_diff.sp_followers': 'sp_followers_diff_monthly',
    'obj.cm_statistics.latest.sp_followers_to_listeners_ratio': 'spfollowers_to_listeners_ratio',
    'obj.cm_statistics.latest.sp_listeners_to_followers_ratio': 'sp_listeners_to_followers_ratio',
    'obj.cm_statistics.latest.sp_monthly_listeners': 'sp_monthly_listeners',
    'obj.cm_statistics.weekly_diff.sp_monthly_listeners': 'sp_monthly_listeners_diff_weekly',
    'obj.cm_statistics.monthly_diff.sp_monthly_listeners': 'sp_monthly_listeners_diff_monthly',
    'obj.cm_statistics.latest.sp_popularity': 'sp_popularity',
    'obj.cm_statistics.weekly_diff.sp_popularity': 'sp_popularity_diff_weekly',
    'obj.cm_statistics.monthly_diff.sp_popularity': 'sp_popularity_diff_monthly',
    'obj.cm_statistics.latest.spotify_ed_playlist_count': 'sp_editorial_playlist_count',
    'obj.cm_statistics.weekly_diff.num_sp_editorial_playlists': 'sp_editorial_playlist_count_diff_weekly',
    'obj.cm_statistics.monthly_diff.num_sp_editorial_playlists': 'sp_editorial_playlist_count_diff_monthly',
    'obj.cm_statistics.latest.spotify_ed_playlist_total_reach': 'sp_editorial_playlist_total_reach',
    'obj.cm_statistics.weekly_diff.sp_editorial_playlist_total_reach': 'sp_editorial_playlist_total_reach_diff_weekly',
    'obj.cm_statistics.monthly_diff.sp_editorial_playlist_total_reach': 'sp_editorial_playlist_total_reach_diff_monthly',
    'obj.cm_statistics.latest.spotify_playlist_count': 'sp_playlist_count',
    'obj.cm_statistics.weekly_diff.num_sp_playlists': 'sp_playlist_count_diff_weekly',
    'obj.cm_statistics.monthly_diff.num_sp_playlists': 'sp_playlist_count_diff_monthly',
    'obj.cm_statistics.latest.spotify_playlist_total_reach': 'sp_playlist_total_reach',
    'obj.cm_statistics.weekly_diff.sp_playlist_total_reach': 'sp_playlist_total_reach_diff_weekly',
    'obj.cm_statistics.monthly_diff.sp_playlist_total_reach': 'sp_playlist_total_reach_diff_monthly',
    'obj.cm_statistics.latest.spotify_popular_playlist_count': 'sp_popular_playlist_count',
    'obj.cm_statistics.latest.spotify_popular_playlist_total_reach': 'sp_popular_playlist_total_reach',
    'obj.cm_statistics.latest.spotify_popular_playlist_tracks': 'sp_popular_playlist_tracks',

    # TikTok Stats
    'obj.cm_statistics.tiktok_followers': 'tt_followers',
    'obj.cm_statistics.weekly_diff.tiktok_followers': 'tt_followers_diff_weekly',
    'obj.cm_statistics.monthly_diff.tiktok_followers': 'tt_followers_diff_monthly',
    'obj.cm_statistics.tiktok_likes': 'tt_likes',
    'obj.cm_statistics.weekly_diff.tiktok_likes': 'tt_likes_diff_weekly',
    'obj.cm_statistics.monthly_diff.tiktok_likes': 'tt_likes_diff_monthly',
    'obj.cm_statistics.latest.tiktok_top_video_comments': 'tt_top_video_comments',
    'obj.cm_statistics.weekly_diff.tiktok_top_video_comments': 'tt_top_video_comments_diff_weekly',
    'obj.cm_statistics.monthly_diff.tiktok_top_video_comments': 'tt_top_video_comments_diff_monthly',
    'obj.cm_statistics.latest.tiktok_top_video_views': 'tt_top_video_views',
    'obj.cm_statistics.weekly_diff.tiktok_top_video_views': 'tt_top_video_views_diff_weekly',
    'obj.cm_statistics.monthly_diff.tiktok_top_video_views': 'tt_top_video_views_diff_monthly',
    'obj.cm_statistics.latest.tiktok_track_posts': 'tt_track_posts',
    'obj.cm_statistics.weekly_diff.tiktok_track_posts': 'tt_track_posts_diff_weekly',
    'obj.cm_statistics.monthly_diff.tiktok_track_posts': 'tt_track_posts_diff_monthly',
}, inplace=True)

# Save to CSV
df.to_csv("ch_artist_metadata.csv", index=False)