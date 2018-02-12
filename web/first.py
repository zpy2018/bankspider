# -*- coding: utf-8 -*-
from flask import render_template
from flask import Flask
from flask import jsonify
from flask import Response
import sql
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def index():
    head = '银行公示'
    return render_template('index.html', head=head)


@app.route('/<city>/<pagenum>')
def cd(city, pagenum):
    res, maxpage = sql.select(city, pagenum)
    pagenum = min(max(1, int(pagenum)), maxpage + 1)
#    print(maxpage)
    pages = [i + 1 for i in range(maxpage + 1)]
    title = res[0][-2] + '公告'
    return render_template('detail.html', infos=res, p=pagenum - 1, n=pagenum + 1, title=title, pages=pages, current=pagenum, city=city)


@app.route('/info/<id>')
def display(id):
    bank = sql.getbank(id)
    backurl = '/' + id[:2] + '/' + str(int(id[2:]) // 10)
    f = open('files/' + id + '.txt', 'r')
    text = f.read()
    f.close()
    result = sql.getlinks(id)
    head = sql.getname(id)
    if text == 'pic':
        pics = result.split('_just_a_split_')
        return render_template('pic.html', pics=pics, head=head)
    links = []
    start = 0
    count = 1
    if result:
        dates = result.split('_just_a_split_')
        for date in dates:
            soup = BeautifulSoup(date)
            kw = soup.a.text
            if 'href' not in soup.a.attrs:
                continue
            url = soup.a.attrs['href']
            length = len(kw)
            if kw not in text:
                continue
            else:
                loc = text[start:].find(kw)
                sym = '{ ' + str(count) + ' }'
                text = text[:loc + start + length] + sym + text[loc + length + start:]
                links.append([sym + kw, url])
                count += 1
                start += loc + length
    return render_template('info.html', links=links, text=text, head=head, bank=bank, backurl=backurl)



# @app.route('/bgp')
# def bgp():
#     image = open('1.jpg', 'rb')
#     resp = Response(image, mimetype='image/jpg')
#     return resp


if __name__ == '__main__':
    app.run(debug=True)
