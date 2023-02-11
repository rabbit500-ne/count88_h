import pytest
from  lib.database_utils import OthelloDb as db

db.initial("./resource/othello.db")

def test_search_duplicate_stage():
    tbl_num = 5
    stage = db.debug_get_stage(tbl_num,2)
    id = db.search_duplicate_stage(tbl_num, stage, stage.id)
    assert id is None

def test_search_duplicate_stage_2():
    tbl_num = 5
    stage = db.debug_get_stage(tbl_num,2)
    id = db.search_duplicate_stage(tbl_num, stage, stage.id)
    assert id is None