from flask import Flask, render_template, request, jsonify
import mysql.connector as my

app = Flask(__name__)

@app.route('/')
def hello():
    props ={}
    return render_template("./index.html", props=props)

@app.route('/search')
def search():
    query = request.args.get("query")
    con = my.connect(host="db", database="viblioteca", user="viblioteca", password="viblioteca")
    try:
        cur = con.cursor()
        try:
            cur.execute("select id, org, title, url, description, filename, tag, width, height, thumbUrl from contents"
                " where description like %s", ("%" + query + "%",))
            result = list()
            for r in cur:
                result.append({"id": r[0], "org": r[1], "title": r[2],
                    "url": r[3], "description": r[4], "filename": r[5],
                    "tag": r[6], "width": r[7], "height": r[8]})
            return jsonify(result)
        finally:
            cur.close()
    finally:
        con.close()
#https://i.vimeocdn.com/video/998078192.webp?mw=900&mh=507

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)