import os
# Flask から importしてflaskを使えるようにする
import sqlite3, datetime as dt
from flask import Flask, render_template, request, redirect, session

# appの名前でFlaskアプリを作っていく
app = Flask(__name__)
# ここまでおまじない

app.secret_key="sunabaco"

@app.route("/")
def init():
    return render_template('init.html')

# DBへの接続
@app.route("/index")
def index():
    conn = sqlite3.connect("maintenance.db")
    c=conn.cursor()
    c.execute("select name from users where id = 1")
    user_info = c.fetchone()
    c.close()
    return render_template("index.html", user = user_info)

#追加の処理/そとアイテム
@app.route("/add/item/soto",methods=["POST"])
def add_post_item_soto():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    item = request.form.get("item")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    tbname_list = []
    for row in tb_list:
        tbname_list.append(row[0])
    if tablename in tbname_list:
        return render_template("error_soto.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,item,tablename))
        c.execute("create table %s (taskid INTEGER, date DATE, task TEXT, notice DATE,PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/soto")

#追加の処理/うちアイテム
@app.route("/add/item/uti",methods=["POST"])
def add_post_item_uti():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    item = request.form.get("item")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    print(tb_list)
    print(type(tb_list))
    print(tb_list[0])
    print(type(tb_list[0]))
    print('---xxx------')
    tbname_list = []
    for row in tb_list:
        print(row[0])
        tbname_list.append(row[0])
    # タプルをリストに変換
    print(tbname_list)
    print(type(tbname_list))
    print('---xxx------')
    print(tablename)
    print(type(tablename))
    print(tablename in tbname_list)
    if tablename in tbname_list:
        return render_template("error_uti.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,item,tablename))
        c.execute("create table %s (taskid INTEGER, date DATE, task TEXT, notice DATE,PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/uti")

#追加の処理/にわアイテム
@app.route("/add/item/niwa",methods=["POST"])
def add_post_item_niwa():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    item = request.form.get("item")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    tbname_list = []
    for row in tb_list:
        tbname_list.append(row[0])
    if tablename in tbname_list:
        return render_template("error_niwa.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,item,tablename))
        c.execute("create table %s (taskid INTEGER, date DATE, task TEXT, notice DATE,PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/niwa")

# DBに保存されているものを表示してみよう
@app.route("/list/soto")
def sotoitem_list():
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # c.execute("select name from users where id = ?" , (user_id,))
    # user_name = c.fetchone()[0]
    c.execute("select id, item from items where ios_id = 1")
    # リスト型にする
    item_list=[]
    # print(c.fetchall())
    for row in c.fetchall():
        #rowの要素を連想配列に記述
        item_list.append({"id":row[0],"item":row[1]})
        # print(item_list)
    c.close()
    return render_template("sotoitem_list.html",sotoitem_list = item_list)

@app.route("/list/uti")
def utiitem_list():
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select id, item from items where ios_id = 0")
    item_list=[]
    for row in c.fetchall():
        item_list.append({"id":row[0],"item":row[1]})
    c.close()
    return render_template("utiitem_list.html",utiitem_list = item_list)

@app.route("/list/niwa")
def niwaitem_list():
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select id, item from items where ios_id = 2")
    item_list=[]
    for row in c.fetchall():
        item_list.append({"id":row[0],"item":row[1]})
    c.close()
    return render_template("niwaitem_list.html",niwaitem_list = item_list)

# DBから通知を表示してみよう
@app.route("/notice/tasklist")
def notice_tasklist():
    today = dt.date.today()
    # today = today.strftime('%Y/%m/%d')
    print(today)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
        print(row[0])
    # row[0]をtable_nameの変数としてselect
        c.execute("select item from items where table_name = ?", (row[0], ))
        notice_item = c.fetchone()[0]
    # noticeがtoday と一致するタスクをセレクト
        c.execute("select date, task, notice from %s where notice == ?" % (row[0]), (today,))
        # c.execute("select date, task, notice from %s where notice BETWEEN(today()-INTERVAL '7 day') ?" % (row[0]))
        ntlist = []
        notice_list = c.fetchall()
        print("----yyy--------")
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
                print(ntlist)
                print("----zzz--------")
    #ntlistの中身をnt_list として連想配列化
                for row3 in ntlist:
                    nt_list.append({"date":row3[0],"task":row3[1],"notice":row3[2]})
                    print(nt_list)

    #noticeをすべてリストできる
        # notice_list = c.fetchall()
        # for row2 in notice_list:
        #     ntlist.append(row2[0])

    print('------???-------')
    c.close()
    return render_template("notice_list.html",nt_list = nt_list, notice_item = notice_item, today = today)
    # return "該当する通知はありません"

# そとアイテムの編集
@app.route("/edit/soto/<int:id>")
def edit_item_soto(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select item from items where id=?", (id,))
    item = c.fetchone()[0]
    c.close()
    item = {"id":id, "item":item}
    return render_template("edit_item_soto.html" , item = item)
    
# 変更したデータでそとアイテム更新
@app.route("/edit/soto", methods = ["POST"])
def update_item_soto():
    item_id = request.form.get("id")
    item_id = int(item_id)
    item = request.form.get("item")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("update items set item=? where id = ?", (item,item_id))
    conn.commit()
    c.close()
    return redirect("/list/soto")
    
# うちアイテムの編集
@app.route("/edit/uti/<int:id>")
def edit_item_uti(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select item from items where id=?", (id,))
    item = c.fetchone()[0]
    c.close()
    item = {"id":id, "item":item}
    return render_template("edit_item_uti.html" , item = item)
    
# 変更したデータでうちアイテム更新
@app.route("/edit/uti", methods = ["POST"])
def update_item_uti():
    item_id = request.form.get("id")
    item_id = int(item_id)
    item = request.form.get("item")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("update items set item=? where id = ?", (item,item_id))
    conn.commit()
    c.close()
    return redirect("/list/uti")

# にわアイテムの編集
@app.route("/edit/niwa/<int:id>")
def edit_item_niwa(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select item from items where id=?", (id,))
    item = c.fetchone()[0]
    c.close()
    item = {"id":id, "item":item}
    return render_template("edit_item_niwa.html" , item = item)
    
# 変更したデータでにわアイテム更新
@app.route("/edit/niwa", methods = ["POST"])
def update_item_niwa():
    item_id = request.form.get("id")
    item_id = int(item_id)
    item = request.form.get("item")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("update items set item=? where id = ?", (item,item_id))
    conn.commit()
    c.close()
    return redirect("/list/niwa")

# そとリストからアイテムの削除
@app.route("/del/soto/<int:id>")
def del_item_soto(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    # print(table_name)
    # print(type(table_name))
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/soto")

# うちリストからアイテムの削除
@app.route("/del/uti/<int:id>")
def del_item_uti(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/uti")

# にわリストからアイテムの削除
@app.route("/del/niwa/<int:id>")
def del_item_niwa(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/niwa")

# DBに保存されているタスクをリストしてみよう（うち／そと）
@app.route("/tasklist/<int:id>")
def tasklist(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select id from items where id = ?" , (id,))
    id = c.fetchone()[0]
    c.execute("select item from items where id = ?" , (id,))
    item = c.fetchone()[0]
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    # print(table_name)
    # table = "table_name"
    c.execute("select taskid, date, task, notice from %s" % (table_name))
    task_list = []
        # # タプル型(task, )から[0]要素を取り出す
    # print(c.fetchall())
    for row in c.fetchall():    
        task_list.append({"taskid":row[0],"date":row[1], "task":row[2],"notice":row[3]})
        # print(task_list)
    c.close()
    return render_template("tasklist.html" , task_list = task_list, table_name = table_name, item = item, id = id)
#     else:
#         return redirect("/login")

# DBに保存されているタスクをリストしてみよう（にわ）
@app.route("/tasklist_niwa/<int:id>")
def tasklist_niwa(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select id from items where id = ?" , (id,))
    id = c.fetchone()[0]
    c.execute("select item from items where id = ?" , (id,))
    item = c.fetchone()[0]
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    # print(table_name)
    # table = "table_name"
    c.execute("select taskid, date, task, photo, notice from %s" % (table_name))
    task_list = []
        # # タプル型(task, )から[0]要素を取り出す
    for row in c.fetchall():    
        task_list.append({"taskid":row[0],"date":row[1], "task":row[2],"photo":row[3],"notice":row[4]})
    c.close()
    return render_template("tasklist_niwa.html" , task_list = task_list, table_name = table_name, item = item, id = id)
#     else:
#         return redirect("/login")

# 追加の処理/タスク（うち／そと）
@app.route("/add/tasklist/<int:id>",methods=["POST"])
def add_post_task(id):
    # user_id = session["user_id"]
    date = request.form.get("date")
    task = request.form.get("task")
    notice = request.form.get("notice")
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
        #()はタプル型
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("insert into %s values (null,?,?,?)" % (table_name), (date,task,notice))
    conn.commit()
    c.close()
    # return render_template("tasklist.html" , task_list = task_list, table_name = table_name, item = item, id = id)
    return redirect("/tasklist/%s" %(id))  

# 追加の処理/タスク（にわ）
@app.route("/add/tasklist_niwa/<int:id>",methods=["POST"])
def add_post_task_niwa(id):
    # user_id = session["user_id"]
    date = request.form.get("date")
    task = request.form.get("task")
    photo = request.form.get("photo")
    notice = request.form.get("notice")
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
        #()はタプル型
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("insert into %s values (null,?,?,?,?)" % (table_name), (date,task,photo,notice))
    conn.commit()
    c.close()
    # return render_template("tasklist.html" , task_list = task_list, table_name = table_name, item = item, id = id)
    return redirect("/tasklist_niwa/%s" %(id))  

# # # 編集変更したデータで更新/タスク/うち、そと
@app.route("/edit/tasklist/<int:id>/<int:taskid>")
def edit_tasklist_get(id,taskid):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select date from %s where taskid=?" % (table_name), (taskid,))
    # task_list = c.fetchall()
    # task_list = []
    # for row in c.fetchall():
    #     task_list.append({"taskid":row[0],"date":row[1],"task":row[2],"notice":row[3]})
    date = c.fetchone()[0]
    c.execute("select task from %s where taskid=?" % (table_name), (taskid,))
    task = c.fetchone()[0]
    c.execute("select notice from %s where taskid=?" % (table_name), (taskid,))
    notice = c.fetchone()[0]
    c.close()
    task_list = {"taskid":taskid, "date":date, "task":task, "notice":notice}
    return render_template("edit_tasklist.html", task_list = task_list, id = id)

@app.route("/edit/tasklist/<int:id>", methods = ["POST"])
def tasklist_update(id):
    taskid = request.form.get("taskid")
    taskid = int(taskid)
    date = request.form.get("date")
    task = request.form.get("task")
    notice = request.form.get("notice")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set date=? where taskid = ?" %(table_name), (date,taskid,))
    c.execute("update %s set task=? where taskid = ?" %(table_name), (task,taskid,))
    c.execute("update %s set notice=? where taskid = ?" %(table_name), (notice,taskid,))
    conn.commit()
    c.close()
    return redirect("/tasklist/%s" %(id))  
    
# # # 編集変更したデータで更新/タスク/にわ
@app.route("/edit/tasklist_niwa/<int:id>/<int:taskid>")
def edit_tasklist_get_niwa(id,taskid):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select date from %s where taskid=?" % (table_name), (taskid,))
    # task_list = c.fetchall()
    # task_list = []
    # for row in c.fetchall():
    #     task_list.append({"taskid":row[0],"date":row[1],"task":row[2],"notice":row[3]})
    date = c.fetchone()[0]
    c.execute("select task from %s where taskid=?" % (table_name), (taskid,))
    task = c.fetchone()[0]
    c.execute("select photo from %s where taskid=?" % (table_name), (taskid,))
    photo = c.fetchone()[0]
    c.execute("select notice from %s where taskid=?" % (table_name), (taskid,))
    notice = c.fetchone()[0]
    c.close()
    task_list = {"taskid":taskid, "date":date, "task":task, "photo":photo, "notice":notice}
    return render_template("edit_tasklist_niwa.html", task_list = task_list, id = id)

@app.route("/edit/tasklist_niwa/<int:id>", methods = ["POST"])
def tasklist_niwa_update(id):
    taskid = request.form.get("taskid")
    taskid = int(taskid)
    date = request.form.get("date")
    task = request.form.get("task")
    photo = request.form.get("photo")
    notice = request.form.get("notice")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set date=? where taskid = ?" %(table_name), (date,taskid,))
    c.execute("update %s set task=? where taskid = ?" %(table_name), (task,taskid,))
    c.execute("update %s set photo=? where taskid = ?" %(table_name), (photo,taskid,))
    c.execute("update %s set notice=? where taskid = ?" %(table_name), (notice,taskid,))
    conn.commit()
    c.close()
    return redirect("/tasklist_niwa/%s" %(id)) 

# タスクリストから タスクの削除(うち/そと)
@app.route("/del/tasklist/<int:id>/<int:taskid>")
def del_tasklist(id,taskid):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from %s where taskid=?" % (table_name), (taskid,))
    c = conn.commit()
    conn.close()
    return redirect("/tasklist/%s" %(id)) 

# タスクリストから タスクの削除(にわ)
@app.route("/del/tasklist_niwa/<int:id>/<int:taskid>")
def del_tasklist_niwa(id,taskid):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from %s where taskid=?" % (table_name), (taskid,))
    c = conn.commit()
    conn.close()
    return redirect("/tasklist_niwa/%s" %(id)) 

# 削除機能
# @app.route("/del/<int:id>")
# def del_task(id):
#     # DBに接続＿DB処理の準備＿SQL文の実行(taskテーブルのidがid（関数の引数)のもの
#     # のみ削除", (id,)
#     # 保存
#     # 接続終了
#     # /list でリダイレクト

#     conn = sqlite3.connect("maintenance.db")
#     c = conn.cursor()
#     c.execute("delete from %s where id=?" %(table_name), (id,))
#     c = conn.commit()
#     conn.close()
#     return redirect("/tasklist")
    

# 2021.6.15 ログイン機能など-----------------------------------------------------------
# 登録機能

# @app.route("/regist", methods = ["GET"])
#     # GETはHTMLを表示するだけ
# def regist_get():
#     return render_template("regist.html")

# @app.route("/regist", methods=["POST"])
# def regist_post():
#     name = request.form.get("name")
#     password = request.form.get("password")
#     # requestでHTML側からデータを受け取る
    
#     conn = sqlite3.connect("maintenance.db")
#     c = conn.cursor()
#     c.execute("insert into users values(null,?,?)",(name,password))
#     conn.commit()
#     c.close()
#     return redirect("/login")

# log in ----------------------------------------------------------

# @app.route("/login",methods=["GET"])
# def login_get():
#     if "user_id" in session:
#         return redirect("/list")
#     else:
#         return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def login_post():
#     name = request.form.get("name")
#     password = request.form.get("password")
# #     # requestでHTML側からデータを受け取る
    
#     conn = sqlite3.connect("maintenance.db")
#     c = conn.cursor()
#     c.execute("select id from users where name = ? and password = ?", (name,password))
#     user_id = c.fetchone()
#     c.close()

# # id取れたかどうかで条件分岐

#     if user_id is None:
#         return render_template("login.html")
#     else:
#         session["user_id"] = user_id[0]
#     #     # クッキーをここで設定
    
    # return redirect("/list")

# ログアウト-----------------------------------------------------------------
# @app.route("/logout")
# def logout():
#     session.pop("user_id", None)
#     return redirect("/login")

#404ページ
@app.errorhandler(404)
def not_found(error):
    return "ページが見つかりません"

#おまじない
if __name__ == "__main__":
    # Flaskが持っている開発用サーバーを実行します。
    app.run(debug=True)