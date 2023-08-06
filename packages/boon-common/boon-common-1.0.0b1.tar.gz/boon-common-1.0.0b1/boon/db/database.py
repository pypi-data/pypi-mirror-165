#!/usr/bin/env python3

# BoBoBo

from dbutils.pooled_db import PooledDB

import boon.db.database_execute as dbe


def get_db(conf, creator):
    if not conf:
        return None

    dbconf = conf.copy()
    dbconf['creator'] = creator
    conn_pool = None

    def _get_conn():
        nonlocal dbconf
        nonlocal conn_pool

        if conn_pool is None:
            conn_pool = PooledDB(**dbconf)
        return conn_pool.connection()

    return _get_conn


def convert_ret(res_all, description):
    rows = []
    if res_all is None:
        return rows
    for res in res_all:
        row = {}
        for i in range(len(description)):
            row[description[i][0]] = res[i]
        rows.append(row)
    return rows


def query(conn, sql, param, auto_close=True):
    def getall(cur):
        return (cur.fetchall(), cur.description)

    sqls = [(sql, param)]
    _, _, ret = dbe.execute_read(conn, sqls, hook_cur=getall)
    if ret:
        return convert_ret(ret[0][0], ret[0][1])
    else:
        return None


def insert(conn, sqls, auto_close=True):
    def getlastid(cur):
        return cur.lastrowid

    return dbe.execute_write(conn, sqls,
                             hook_cur=getlastid, auto_close=auto_close)


def update(conn, sql, param, auto_close=True):
    sqls = [(sql, param)]
    return dbe.execute_write(conn, sqls, auto_close=auto_close)
