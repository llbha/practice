import sqlite3, re, json

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
sql = """CREATE TABLE IF NOT EXISTS journal_info(id INTEGER PRIMARY KEY ,name VARCHAR ,en_name VARCHAR ,index_info VARCHAR ,basic_info MESSAGE_TEXT ,publish_info MESSAGE_TEXT ,evaluate_info MESSAGE_TEXT ,pic_url VARCHAR )"""
cursor.execute(sql)
conn.commit()
with open('1.txt', encoding='utf-8') as f:
    str = f.read()
    str = str.replace(' ', '').replace('\ufeff', '').strip('(').strip(')')
    str = str.split('),(')
    type_list = []
    for each in str:
        pattern = re.compile(r"'(.*?)'", re.S)
        rs = re.findall(pattern, each)
        id = re.search('\d+', each).group()
        name = rs[0]+'('+rs[1]+')'
        index_info = rs[2]
        basic_info = rs[3]
        publish_info = rs[4]
        evaluate_info = rs[5]
        pic_url = rs[6]

        # basic_info字符转json
        basic_info = basic_info.split('\\n')
        if len(basic_info) == 4:
            en_name = basic_info[0].split('：')[-1].strip()
            basic_info = basic_info[1::]
        else:
            en_name = '无'
        a = basic_info[0].split('：')[-1]
        b = basic_info[1].split('ISSN：')[0].split('：')[-1]
        c = basic_info[1].split('ISSN：')[-1]
        d = basic_info[2].split('出版地：')[0].split('：')[-1]
        e = basic_info[2].split('出版地：')[-1].split('语种')[0]
        f = basic_info[2].split('语种：')[-1].split('开本：')[0]
        g = basic_info[2].split('开本：')[-1].split('邮发代号：')[0]
        h = basic_info[2].split('邮发代号：')[-1].split('创刊时间：')[0]
        i = basic_info[2].split('创刊时间：')[-1]
        basic_info = {
            '主办单位': a,
            '出版周期': b,
            'CN': c,
            'ISSN': d,
            '出版地': e,
            '语种': f,
            '开本': g,
            '邮发代号': h,
            '创刊时间': i,
        }
        basic_info = json.dumps(basic_info, ensure_ascii=False)

        # publish_info字符转json
        publish_info = publish_info.split(r"\n")
        for i in range(publish_info.count('')):
            publish_info.remove('')
        publish_info = {
            '专辑名称': publish_info[0].split('：')[-1],
            '专题名称': publish_info[1].split('：')[-1],
            '出版文献量': publish_info[2].split('：')[-1],
            '总下载次数': publish_info[3].split('总被引次数：')[0].split('：')[-1],
            '总被引次数': publish_info[3].split('总被引次数：')[-1]
        }
        publish_info = json.dumps(publish_info, ensure_ascii=False)

        # evaluate_info字符转json
        evaluate_info = evaluate_info.split(r"\n")
        for i in range(evaluate_info.count('')):
            evaluate_info.remove('')
        a = evaluate_info[0].split(':')[-1]
        b = evaluate_info[1].split('：')[-1]
        if '该刊被以下数据库收录：' in evaluate_info[2]:
            c = evaluate_info[3].split('来源期刊：')[0]
            if '期刊荣誉：' not in evaluate_info[3]:
                d = evaluate_info[3].split('来源期刊：')[-1]
                e = '无'
            else:
                d = evaluate_info[3].split('来源期刊：')[-1].split('期刊荣誉：')[0]
                e = evaluate_info[3].split('期刊荣誉：')[-1]
        elif '来源期刊：' in evaluate_info[2]:
            c = evaluate_info[2].split('来源期刊：')[0]
            d = evaluate_info[3]
            e = '无'
        else:
            c = '无',
            d = '无',
            e = evaluate_info[3]
        evaluate_info = {
            '（2018版）复合影响因子': a,
            '（2018版）综合影响因子': b,
            '该刊被以下数据库收录': c,
            '来源期刊': d,
            '期刊荣誉': e
        }
        evaluate_info = json.dumps(evaluate_info, ensure_ascii=False)

        sql = """INSERT INTO journal_info(`name`, en_name, index_info, basic_info, publish_info, evaluate_info, pic_url)VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (name, en_name, index_info, basic_info, publish_info, evaluate_info, pic_url)
        cursor.execute(sql)
        conn.commit()

    # 输出收录类型
        index_info = rs[2].split('|')
        for x in index_info:
            type_list.append(x)
    print(' '.join(list(set(type_list))))
    f.close()
cursor.close()
conn.close()