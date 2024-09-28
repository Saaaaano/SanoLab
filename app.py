from flask import Flask, render_template,request,redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename
import densukeanalyzer as da

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/densuke-analyzer')
def dana():
    return render_template('densuke-analyzer.html')

@app.route('/url-send', methods=['GET','POST'])
def urlsend():
    if request.method == 'POST':
        # URL情報を取得
        url = request.form['url-input']
        # 伝助のURL以外は受け付けない
        if "https://densuke.biz/list" in url:
            try:
                # html情報を取得
                soup = da.get_data_soup(url)
                # 入力者の名前とマーク情報を取得
                names, header_items = da.get_data_header(soup)
                # イベントの説明文を取得
                expl = da.get_expl(soup)
                # 記入者のコメントを取得
                comments = da.get_comment
                # 表を取得
                lines = da.get_data_schedule(soup, names, header_items)
                return render_template('densuke-analyzer.html', names=names, heder_items=header_items, expl=expl, comments=comments, lines=lines)
            except AttributeError:
                # 伝助URLで無効なもの
                return render_template('densuke-analyzer.html')
        else:
            return render_template('densuke-analyzer.html')
    else:
        return render_template('densuke-analyzer.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
