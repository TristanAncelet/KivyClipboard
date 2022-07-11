__all__ = [
    "get_clipboard_names",
    "get_clips",
    "get_clips_from_board",
    "change_clip_board",
    "update_clip_ordering",
    "insert_new_clip"
]
#Get Quries
get_clipboard_names = "SELECT board_name FROM board;"
get_clips = "SELECT * FROM clips"
get_clips_from_board = "SELECT * FROM clips WHERE board_id = ?;"
get_clip_column_names = "PRAGMA table_info(clips);"

#Update Queries
change_clip_board = "UPDATE clips SET board_id = ? WHERE clip_id = ?;"
update_clip_ordering = "UPDATE clip_ordering SET clip_index = ? WHERE clip_id = ? AND board_id = ?;"

#Insert Queries
insert_new_clip = "INSERT INTO clips (clip_type, clip_data, board_id) VALUES (?, ?, ?);"