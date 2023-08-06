#!/usr/bin/env python3

# BoBoBo

def execute(conn, sqls, auto_commit, auto_close, hook_cur):
    if None is conn:
        return None

    cur = None
    try:
        cur = conn.cursor()
        ret = []
        for tp in sqls:
            if tp[1]:
                print(str(tp))
                cur.execute(tp[0], tp[1])
                if hook_cur:
                    ret.append(hook_cur(cur))
            else:
                cur.execute(tp[0])
                if hook_cur:
                    ret.append(hook_cur(cur))
        if auto_commit:
            conn.commit()
        return conn, cur, ret
    except Exception as e:
        if auto_commit and conn:
            conn.rollback()
        raise e
    finally:
        if auto_close:
            if cur:
                cur.close()
            if auto_close and conn:
                conn.close()


def execute_read(conn, sqls, auto_commit=True, auto_close=True, hook_cur=None):
    return execute(conn, sqls, auto_commit, auto_close, hook_cur)


def execute_write(conn, sqls,
                  auto_commit=True, auto_close=True, hook_cur=None):
    return execute(conn, sqls, auto_commit, auto_close, hook_cur)
