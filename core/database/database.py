from pathlib import Path
import sql_quries as quries
import sqlite3

user_data_folder = Path.home() / ".data"
if not user_data_folder.exists():
    user_data_folder.mkdir()

database_file = user_data_folder / "clipboard.db"
if not database_file.exists():
    database_file.touch()

class Clip:
    def __init__(self, query_result) -> None:
        self.__dict__.update(query_result)

    @property
    def Type(self):
        return self.clip_type
    
    @property
    def Id(self):
        return self.clip_id
    
    @property
    def Data(self):
        return self.clip_data
    
    @property
    def Board_ID(self):
        return self.board_id
    
    def Insert_Into_Board(self, board_id):
        self.board_id 

class Board:
    clips = list
    database = Non
    
    def __init__(self, database:'Database', board_name:str, clip_results:list) -> None:
        self.database = database
        self.board_name = board_name
        self.clips = clip_results



class Database:
    _conn = sqlite3.connect(str(database_file.absolute()))
    _cur = _conn.cursor()

    board = Board
    def LoadData(self):
        pass

    @property
    def BoardNames(self):
        self._cur.execute(quries.get_clipboard_names)
        return self._cur.fetchall()

    def LoadBoard(self, board_id:int) -> None:
        self.board()

    def GetClipsFromBoard(self, board_id:int = 1) -> list[Clip]:
        self._cur.execute(quries.get_clip_column_names)
        column_names = [itemset[1] for itemset in self._cur.fetchall()]

        self._cur.execute(quries.get_clips_from_board, (board_id,))
        results = self._cur.fetchall()

        clips_to_return = list()

        for dataset in results:
            clips_to_return.append({column_name:value for column_name, value in zip(column_names, dataset)})
        
        return [Clip(dataset) for dataset in clips_to_return]
