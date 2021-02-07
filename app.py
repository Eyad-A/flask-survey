from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def index():
    return render_template("index.html", survey=satisfaction_survey)

@app.route('/begin', methods=["POST"])
def begin():
    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def handle_question():
    choice = request.form['answer']
    responses.append(choice)
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect (f"/questions/{len(responses)}")
        

@app.route('/questions/<int:qid>')
def show_question(qid):
    """ Trying to access the questions too soon """
    if (responses is None):
        flash("Please start from the beginning")
        return redirect('/')
    
    """ Finished answering all the questions """
    if (len(responses) == len(satisfaction_survey.questions)):
        flash("Survey has been completed, thank you")
        return redirect('/complete')

    """ Trying to answer questions out of order """
    if (len(responses) != qid):
        flash("Nice try. No messing with the URL please")
        return redirect(f'/questions/{len(responses)}')
    
    question = satisfaction_survey.questions[qid]
    return render_template("question.html", question=question, qid=qid)

@app.route('/complete')
def complete():
    return render_template("thankyou.html")