import count88 as c88
from lib.common import *
from dbsetup import create_db, seed

def main():
    dbpath = f"./resource/speed_{get_current_time_str()}.db"
    # db作成
    create_db(dbpath)
    seed(dbpath)
    
    # 開始
    with TimeMeasur() as tmsr :
        args = type('MyClass', (), {})()
        args.start = 4
        args.depth = 10
        args.dbpath = dbpath
        args.notmem = True
        c88.main(args)
    print(tmsr.result)

if __name__ == "__main__":
    main()