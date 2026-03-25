from flask import Flask, render_template, request, session
import json
import random

app = Flask(__name__)
app.secret_key = "secret123"

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def home():
    session.clear()
    return render_template("home.html")

@app.route("/game/<category>", methods=["GET", "POST"])
def game(category):

    if category == "movie":
        data = load_data("movies.json")
    elif category == "cricket":
        data = load_data("cricket.json")
    else:
        return "Invalid category"

    if "score" not in session:
        session["score"] = 0

    # Load question if not exists
    if "current" not in session:
        session["current"] = random.choice(data)
        session["answered"] = False

    current = session["current"]
    message = ""
    show_next = False

    if request.method == "POST":

        # NEXT BUTTON CLICK
        if "next" in request.form:
            session["current"] = random.choice(data)
            session["answered"] = False
            return render_template("game.html",
                                   clue=session["current"]["clue"],
                                   dialogue=session["current"]["dialogue"],
                                   message="",
                                   score=session["score"],
                                   category=category,
                                   show_next=False)

        # ANSWER SUBMITTED
        if not session["answered"]:
            user_answer = request.form["answer"].strip().lower()

            if user_answer in current["answer"]:
                session["score"] += 1
                message = "✅ Correct!"
            else:
                message = f"❌ Wrong! Correct answer is: {current['answer'][0]}"

            session["answered"] = True
            show_next = True

    return render_template("game.html",
                           clue=current["clue"],
                           dialogue=current["dialogue"],
                           message=message,
                           score=session["score"],
                           category=category,
                           show_next=show_next)
    
if __name__ == "__main__":
    app.run(debug=True)