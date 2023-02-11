import pytest
import lib.database_utils as db
import lib.othello_utils as ou
import count88.py as c88

TEST_SEARCH_DUPLICATE_STAGE = [

]


# @pytest.mark.parametrize("")
def test_search_duplicate_stage():
    tbl_num = 5
    stage = db.debug_get_stage(cls, tbl_num, 2)
    assert c88.search_duplicate_stage(table_num, stage)