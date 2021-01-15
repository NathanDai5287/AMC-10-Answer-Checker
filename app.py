from flask import Flask, request, render_template

from answer import grade, cutoff, key

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/score', methods=['GET', 'POST'])
def score():
	if (request.method == 'POST'):
		answers = request.form.get('answers')

		with open('answers.csv', 'w') as f: # BUG: sometimes it reads the file before it writes and the score is 0
			print(answers, end='write')
			[f.write(i + '\n') for i in answers.split(',')]

		return ''
	else:
		with open('answers.csv') as f:
			answers = [i.strip() for i in f.readlines()]
			print(answers, end='final')

		score, correct, incorrect, skipped = grade(answers, key)

		return render_template('score.html', score=score) # TODO: pass parameters here

if __name__ == "__main__":
	app.run(debug=True)
