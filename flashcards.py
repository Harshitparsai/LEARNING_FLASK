from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
from model import db, save_db

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("welcome.html", cards=db)


@app.route("/cards/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template("cards.html", card=card, index=index, maxindex=len(db)-1)
    except:
        abort(404)


@app.route("/add/cards", methods=["GET", "POST"])
def addcard():
    if request.method == "GET":
        return render_template("add_cards.html")
    else:
        card = {"question": request.form["question"],
                "answer": request.form["answer"]}
        db.append(card)
        save_db()
        return redirect(url_for("card_view", index=len(db)-1))


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def removeCard(index):
    try:
        if request.method == "GET":

            return render_template("remove_card.html", card=db[index], index=index)

        else:
            del db[index]
            save_db()
            return redirect(url_for("welcome"))
    except:
        abort(404)


@app.route('/api/cards')
def listPage():
    return jsonify(db)


@app.route('/api/card/<int:index>')
def detailPage(index):
    try:
        return db[index]
    except:
        abort(404)
