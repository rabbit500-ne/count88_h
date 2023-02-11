import os, time, argparse
import lib.othello_utils as ot
from  lib.database_utils import OthelloDb as db
from lib.define import DuplicateType, Stage, BLACK, WHITE, Status
from lib.common import *

DB_PATH = "./resource/othello.db"

def create_next_stage(tbl_num, stage : Stage):
    selected = 0
    can = ot.search(stage.board, stage.hand)
    next_hand = not stage.hand
    if can != 0:
        next_stage_ids = []
        for _ in range(bin(can).count('1')):
        # while can != selected:
            move = ot.select_hand(can, selected)
            next_board = ot.reverse(stage.board, move, stage.hand)
            next_stage = Stage(
                tbl_num = tbl_num +1,
                hand = next_hand,
                board = next_board,
                pass_count = 0,
            )
            id = db.create_stage(tbl_num + 1, next_stage)
            next_stage_ids.append(f"{tbl_num + 1}-{id}")
            selected += move
        db.set_next_stages(tbl_num, stage, next_stage_ids)
    elif stage.pass_count == 1:
        # 終了
        db.set_end(stage.tbl_num, stage.board)
    elif stage.pass_count == 0:
        # 差し手なし。パス。
        next_stage = Stage(
                tbl_num = tbl_num,
                hand = next_hand,
                board = stage.board,
                pass_count = 1,
            )
        id = db.create_stage(next_stage.tbl_num, next_stage)
        db.set_next_stage(tbl_num, stage, [f"{tbl_num}-{id}"])
    else:
        raise Exception()

def get_target_stage(tbl_num=4):
    return db.get_target_stage(tbl_num)

def cnv_duplicate_stage(stage, duplicate_type):
    if duplicate_type == DuplicateType.POINT_TARGET_90:
        return Stage(
            tbl_num=stage.tbl_num,
            hand= stage.hand,
            board= ot.rotate90(stage.board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.POINT_TARGET_180:
        return Stage(
            tbl_num=stage.tbl_num,
            hand= stage.hand,
            board= ot.rotate180(stage.board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.POINT_TARGET_270:
        return Stage(
            tbl_num=stage.tbl_num,
            hand=stage.hand,
            board= ot.rotate270(stage.board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.LINE_SYMMETRY:
        return Stage(
            tbl_num=stage.tbl_num,
            hand=stage.hand,
            board= ot.x_axis_reflect(stage.board),
            pass_count=stage.pass_count)

    elif duplicate_type == DuplicateType.LINE_SYMMETRY_PT_90:
        board = ot.x_axis_reflect(stage.board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand=stage.hand,
            board= ot.rotate90(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.LINE_SYMMETRY_PT_180:
        board = ot.x_axis_reflect(stage.board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand=stage.hand,
            board= ot.rotate180(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.LINE_SYMMETRY_PT_270:
        board = ot.x_axis_reflect(stage.board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand=stage.hand,
            board= ot.rotate270(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.COLOR_INVERSION:
        return Stage(
            tbl_num=stage.tbl_num,
            hand= BLACK if stage.hand == WHITE else WHITE,
            board= ot.color_inversion(stage.board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.CI_POINT_TARGET_90:
        board = ot.color_inversion(stage.board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand= BLACK if stage.hand == WHITE else WHITE,
            board= ot.rotate90(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.CI_POINT_TARGET_180:
        board = ot.color_inversion(stage.board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand= BLACK if stage.hand == WHITE else WHITE,
            board= ot.rotate180(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.CI_POINT_TARGET_270:
        board = ot.color_inversion(stage.board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand= BLACK if stage.hand == WHITE else WHITE,
            board= ot.rotate270(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.CI_LINE_SYMMETRY:
        board = ot.color_inversion(stage.board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand= BLACK if stage.hand == WHITE else WHITE,
            board= ot.x_axis_reflect(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.CI_LINE_SYMMETRY_PT_90:
        board = ot.color_inversion(stage.board)
        board = ot.x_axis_reflect(board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand= BLACK if stage.hand == WHITE else WHITE,
            board= ot.rotate90(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.CI_LINE_SYMMETRY_PT_180:
        board = ot.color_inversion(stage.board)
        board = ot.x_axis_reflect(board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand= BLACK if stage.hand == WHITE else WHITE,
            board= ot.rotate180(board),
            pass_count=stage.pass_count)
    elif duplicate_type == DuplicateType.CI_LINE_SYMMETRY_PT_270:
        board = ot.color_inversion(stage.board)
        board = ot.x_axis_reflect(board)
        return Stage(
            tbl_num=stage.tbl_num,
            hand= BLACK if stage.hand == WHITE else WHITE,
            board= ot.rotate270(board),
            pass_count=stage.pass_count)
    else:
        raise Exception(duplicate_type)

def search_duplicate_stage(table_num, stage):
    for duplicate_type in DuplicateType:
        if duplicate_type == DuplicateType.UNDECIDED:
            continue
        cnv_stage = cnv_duplicate_stage(stage, duplicate_type)
        duplicate_id = db.search_duplicate_stage(table_num, cnv_stage, stage.id)
        if duplicate_id is not None:
            print(f"duplicate_id : {duplicate_id} @@@@")
            # 重複あり
            stage.duplicate_type = duplicate_type
            stage.duplicate_status = Status.DUPLICATE
            stage.duplicate_stage_id = duplicate_id
            stage.status = Status.DUPLICATE
            db.set_duplicate_type(table_num, stage)
            return True
    else:
        # 重複なし
        stage.status = Status.ORIGINAL
        print("original")
        db.set_duplicate_type(table_num, stage)
        return False

def counter(tbl_num):
    
    db.initial(DB_PATH)

    while True:
        stage = get_target_stage(tbl_num)
        if stage is None:
            break
        if search_duplicate_stage(tbl_num, stage):
            # 重複あり
            continue
        else:
            # 重複なし
            create_next_stage(tbl_num, stage)
            pass

    print("End")


class Data():
    def __init__(self):
        self.lines = []

    def set(self, table_num, time, size):
        self.lines.append(f"s{table_num}, {time}, {size}\n")

    def dump(self, file_path):
        with open(file_path, "w") as f:
            f.writelines(self.lines)


def main(args):
    data = Data()
    for i in range(args.start, args.start + args.depth):
        s = time.time()
        counter(i)
        e = time.time() - s
        size = os.path.getsize(DB_PATH)
        data.set(i, e, size)

    data.dump(f"./resource/{get_current_time_str()}_time.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is a sample script using argparse.")
    parser.add_argument("-s", "--start", type=int, default=4, required=True, help="Start stage number")
    parser.add_argument("-d", "--depth", type=int, default=1, help="Depth from start stage.")

    main(parser.parse_args())





        
    
    
