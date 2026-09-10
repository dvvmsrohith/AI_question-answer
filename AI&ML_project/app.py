from flask import Flask, render_template, request, redirect, url_for
from transformers import pipeline
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------------------------------------
# Load AI Question Answering Model
# ---------------------------------------

qa_model = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)


# ---------------------------------------
# Database
# ---------------------------------------

def create_database():

    conn = sqlite3.connect("qa_history.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paragraph TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            confidence REAL,
            date_time TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


# ---------------------------------------
# Home Page
# ---------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""
    confidence = ""
    paragraph = ""
    question = ""

    if request.method == "POST":

        paragraph = request.form["paragraph"]
        question = request.form["question"]

        if paragraph.strip() and question.strip():

            # Ask AI
            result = qa_model(
                question=question,
                context=paragraph
            )

            answer = result["answer"]

            confidence = round(
                result["score"] * 100,
                2
            )

            # Save question and answer
            conn = sqlite3.connect("qa_history.db")

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO history
                (paragraph, question, answer, confidence, date_time)
                VALUES (?, ?, ?, ?, ?)
            """, (
                paragraph,
                question,
                answer,
                confidence,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            conn.commit()
            conn.close()

    return render_template(
        "index.html",
        answer=answer,
        confidence=confidence,
        paragraph=paragraph,
        question=question
    )


# ---------------------------------------
# Question History
# ---------------------------------------

@app.route("/history")
def history():

    conn = sqlite3.connect("qa_history.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM history
        ORDER BY id DESC
    """)

    history_data = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=history_data
    )


# ---------------------------------------
# View One Saved Question
# ---------------------------------------

@app.route("/history/<int:question_id>")
def view_question(question_id):

    conn = sqlite3.connect("qa_history.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM history
        WHERE id = ?
    """, (question_id,))

    question_data = cursor.fetchone()

    # Get previous question
    cursor.execute("""
        SELECT id FROM history
        WHERE id < ?
        ORDER BY id DESC
        LIMIT 1
    """, (question_id,))

    previous = cursor.fetchone()

    # Get next question
    cursor.execute("""
        SELECT id FROM history
        WHERE id > ?
        ORDER BY id ASC
        LIMIT 1
    """, (question_id,))

    next_question = cursor.fetchone()

    conn.close()

    if question_data is None:
        return redirect(url_for("history"))

    return render_template(
        "history.html",
        question_data=question_data,
        previous=previous,
        next_question=next_question
    )


# ---------------------------------------
# Run Flask
# ---------------------------------------

if __name__ == "__main__":
    app.run(debug=True)