# coding=utf-8
import time
from pymysql import connect
import re
import urllib.parse
import logging
from mini_mysql import MiniMysql

# URL_FUNC_IDCT = {
#     '/index.py':index,
#     '/center.py':center,
# 

URL_FUNC_IDCT = dict()
s = MiniMysql('localhost', 3306, 'root', 'mysql', 'stock_db')

def route(url):
    def set_func(func):
        URL_FUNC_IDCT[url] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func

@route(r'/index.html')
def index(ret):
    with open('./templates/index.html') as f:
        content = f.read()
    sql = "select * from info;"

    stock_infos = s.select_all(sql)

    tr_template = """<tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>
                            <input type="button" value="添加" id="toADD" name="toAdd" systemidvaule="%s">
                        </td>
                    </tr>
                    """
    html = ""
    for line_info in stock_infos:
        html += tr_template % (line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6], line_info[7], line_info[1])
    # print(html)
    content = re.sub(r"\{%content%\}", html, content)
    return content

@route(r'/center.html')
def center(ret):
    with open('./templates/center.html') as f:
        content = f.read()

    sql = "select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id=f.info_id;"

    stock_infos = s.select_all(sql)

    tr_template = """<tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>
                            <a type="button" class="btn btn-default btn-xs" href="/update/%s.html">
                                <span class="glyphicon glyphicon-star" aria-hidden="true"></span>修改
                            </a>
                        </td>
                        <td>
                            <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                        </td>
                    </tr>"""
    html = ""
    for line_info in stock_infos:
        html += tr_template % (line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6], line_info[0], line_info[0])
    content = re.sub(r"\{%content%\}", html, content)

    return content

@route(r"/add/(\d+)\.html")
def add_fouce(ret):
    # 获取股票号
    stock_code =ret.group(1)
    # return stock_code

    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = "select * from info where code=%s;"
    cs.execute(sql, (stock_code,))
    if not cs.fetchone():  # 验证是否存在该数据
        cs.close()
        conn.close()
        return "please stop"
    else:
        sql = "select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"
        cs.execute(sql, (stock_code,))
        if cs.fetchone():  # 验证是否存在该数据
            cs.close()
            conn.close()
            return "be followed"
        sql = "insert into focus (info_id) select id from info where code=%s;"
        cs.execute(sql, (stock_code,))
        conn.commit()
        cs.close()
        conn.close()
        return "ok"

@route(r"/del/(\d+)\.html")
def add_fouce(ret):
    
    stock_code =ret.group(1)  # 获取股票号
    # sql = "select * from info where code=%s;"
    s.add_follow(sql, stock_code)
    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = "select * from info where code=%s;"
    cs.execute(sql, (stock_code,))
    if not cs.fetchone():  # 验证是否存在该数据
        cs.close()
        conn.close()
        return "please stop"
    else:
        sql = "select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"
        cs.execute(sql, (stock_code,))

        if not cs.fetchone():  # 验证是否存在该数据
            cs.close()
            conn.close()
            return "not follow"
        sql = "delete from focus where info_id = (select id from info where code=%s);"
        cs.execute(sql, (stock_code,))
        conn.commit()
        cs.close()
        conn.close()
        return "ok"

@route(r"/update/(\d+)\.html")
def show_update_page(ret):
    stock_code =ret.group(1)

    with open('./templates/update.html') as f:
        content = f.read()

    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = "select f.note_info from focus as f inner join info as i on i.id=f.info_id where i.code=%s;"
    cs.execute(sql, (stock_code,))
    note_info = cs.fetchone()[0]
    cs.close()
    conn.close()

    
    content = re.sub(r"\{%note_info%\}", note_info, content)
    content = re.sub(r"\{%code%\}", stock_code, content)
    return content

@route(r"/update/(\d+)/(.*?)\.html")
def save_update_page(ret):
    stock_code =ret.group(1)
    comment = ret.group(2)
    comment = urllib.parse.unquote(comment)


    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = "update focus set note_info=%s where info_id = (select id from info where code=%s);"
    cs.execute(sql, (comment, stock_code,))
    conn.commit()
    cs.close()
    conn.close()

    return "ok"

def application(environm, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    file_name = environm['PATH_INFO']

    logging.basicConfig(level=logging.INFO, filename='./log.txt', filemode='a', format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    logging.info('访问的是---%s' % file_name)
    try: 
        for url, func in URL_FUNC_IDCT.items():
            ret = re.match(url, file_name)
            if ret:
                return func(ret)
        else:
            logging.warning("no found ---%s" % file_name)
            return "no found ---%s" % file_name
    except Exception as e:
        logging.warning(e)

    # if file_name == '/index.py':
    #     return index()
    # elif file_name == '/center.py':
    #     return center()
    # else:
    #     return 'hello world'
