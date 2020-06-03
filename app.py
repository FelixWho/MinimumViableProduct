from flask import Flask, request, render_template
import IntentLoader

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = IntentLoader.getResult(text)
    return processed_text