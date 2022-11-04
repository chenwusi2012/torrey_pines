from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        query = request.form.get("query")
        query = query.replace(" ", "+")
        return redirect(url_for('/result/'+query))
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
