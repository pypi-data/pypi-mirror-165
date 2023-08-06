"""
A script that holds the definitions of the views in hoodat
"""

view_queries = {}

view_queries[
    "single_view_labels"
] = """
SELECT
    cl.character_label_id,
    cl.character_id,
    cl.timestamp_labelled,
    cl.object_id,
    c.character_name,
    c.actor_id,
    a.actor_name,
    c.series_id,
    s.series_name,
    o.object_number,
    o.object_cascade,
    o.object_x,
    o.object_y,
    o.object_w,
    o.object_h,
    o.video_id,
    v.video_name,
    v.video_type,
    o.episode_id,
    o.frame_id,
    f.frame_number,
    e.episode_number,
    s2.season_id,
    s2.season_number
FROM character_labels cl
LEFT JOIN `characters` c
ON cl.character_id = c.character_id
LEFT JOIN `actors` a
ON c.actor_id = a.actor_id
LEFT JOIN series s
ON c.series_id = s.series_id
LEFT JOIN objects o
ON cl.object_id = o.object_id
LEFT JOIN videos v
ON o.video_id = v.video_id
LEFT JOIN frames f
ON o.frame_id = f.frame_id
LEFT JOIN episodes e
ON o.episode_id = e.episode_id
LEFT JOIN seasons s2
ON e.season_id = s2.season_id
"""

view_queries[
    "single_view_frames"
] = """
SELECT
    f.frame_id,
    f.frame_number,
    s.series_name,
    f.video_id,
    v.video_name,
    v.video_type,
    e.episode_id,
    e.episode_number,
    s2.season_id,
    s2.season_number
FROM frames f
LEFT JOIN videos v
ON f.video_id = v.video_id
LEFT JOIN episodes e
ON v.episode_id = e.episode_id
LEFT JOIN series s
ON v.series_id = s.series_id
LEFT JOIN seasons s2
ON e.season_id = s2.season_id
"""


if __name__ == "__main__":
    import os
    from hoodat_utils.hoodat_sqlalchemy import HoodatSqlalchemy

    uri = os.environ.get("HOODAT_SQLALCHEMY_URI")
    hsa = HoodatSqlalchemy(sqlalchemy_database_uri=uri)
    create_view_result = hsa.create_views(views_obj=view_queries, overwrite=True)
    print(create_view_result)
