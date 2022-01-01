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
    sort = request.args.get("sort")
    con = my.connect(host="db", database="viblioteca", user="viblioteca", password="viblioteca")
    try:
        cur = con.cursor()
        try:
            q = "select id, org, title, description, width, height, " \
                "type, url, embeddable, thumbUrl, indexText, viewCount, likeCount, "\
                "publishedAt from contents" \
                " where LOWER(indexText) like %s"
            if sort == "viewCount":
                q += " order by viewCount desc"
            elif sort == "likeCount":
                q += " order by likeCount desc"
            else:
                q += " order by publishedAt desc"
            cur.execute(q, ("%" + query.lower() + "%",))
            result = list()
            for r in cur:
                result.append({"id": r[0], "org": r[1], "title": r[2],
                    "description": r[3], "width": r[4], "height": r[5],
                    "type": r[6], "url": r[7], "embeddable": r[8] != 0,
                    "thumbUrl": r[9], "indexText": r[10],
                    "viewCount": r[11], "likeCount": r[12],
                    "publishedAt": r[13].strftime("%Y-%m-%d")})
            return jsonify(result)
        finally:
            cur.close()
    finally:
        con.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)