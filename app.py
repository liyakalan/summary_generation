from flask import Flask, render_template, request
from summary import summary_generation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET','POST'])
def generate():
    if request.method=='POST':
        rawtext = request.form['rawtext']
        summary, original_txt, len_orig_txt, len_summary = summary_generation(rawtext)

    return render_template('summary.html', summary=summary, original_txt=original_txt, len_orig_txt=len_orig_txt, len_summary=len_summary)

if __name__ == "__main__":
    app.run(debug=True)

