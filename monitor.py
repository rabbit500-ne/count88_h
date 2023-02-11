import pytest
from  lib.database_utils import OthelloDb as db
import lib.othello_utils as ot
from lib.define import DuplicateType
import count88

db.initial("./resource/othello.db")


def print_stage(tbl_num, id):
    stage = db.debug_get_stage(tbl_num,id)
    print(stage.board.b)
    ot.print_board_wb(stage.board)
    cnv_stage = count88.cnv_duplicate_stage(stage, DuplicateType.LINE_SYMMETRY_PT_270)
    print(cnv_stage.board.str_b )
    print(cnv_stage.board.str_w)
    duplicate_id = db.search_duplicate_stage(5, cnv_stage, stage.id)
    print(f"duplicate_id : {duplicate_id}")
    ot.print_board_wb(cnv_stage.board)

if __name__ == "__main__":
    print_stage(5,1)
    print_stage(5,2)
    
