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
            cur.execute("select id, org, title, description, width, height, "
                "type, url, thumbUrl, indexText from contents"
                " where LOWER(indexText) like %s"
                " order by id", ("%" + query.lower() + "%",))
            result = list()
            for r in cur:
                result.append({"id": r[0], "org": r[1], "title": r[2],
                    "description": r[3], "width": r[4], "height": r[5],
                    "type": r[6], "url": r[7], "thumbUrl": r[8],
                    "indexText": r[9]})
            return jsonify(result)
        finally:
            cur.close()
    finally:
        con.close()
#https://i.vimeocdn.com/video/998078192.webp?mw=900&mh=507

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)