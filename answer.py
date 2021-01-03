from typing import Tuple
from selectorlib import Extractor
from pprint import pformat
import json
import requests
import pandas as pd

def summarize(score: int, cutoff: int, correct: dict, incorrect: dict, skipped: dict) -> str:
	"""formats information

	Args:
		score (int): score on test
		cutoff (int): cutoff of test
		correct (dict): key == question number, value == correct answer
		incorrect (dict): key == question number, value == correct answer
		skipped (dict): key == question number, value == correct answer

	Returns:
		str: writable and formatted string containing all the necessary information
	"""

	summary = ''

	summary += f'Score: {score}\n'
	summary += f'Cutoff: {cutoff}\n\n'

	summary += f'Correct: {len(correct)}\n'
	summary += f'\t{list(correct)}\n\n'
	summary += f'Incorrect: {len(incorrect)}\n'
	summary += f'\t{list(incorrect)}\n\n'
	summary += f'Skipped: {len(skipped)}\n'
	summary += f'\t{list(skipped)}\n'

	if (score != 150):
		summary += '\nCorrect Answers: \n'

		missed = {**incorrect, **skipped}
		summary += pformat(missed, indent=4, width=1).upper().replace('{', ' ').replace('}', ' ').replace(',', '').replace("'", ' ') + '\n'

	return summary

def grade(answers: list, key: list) -> Tuple[dict]:
	"""calculates the score on the test

	Args:
		answers (list): my answers
		key (list): the actual answers

	Returns:
		tuple[dict]: score, correct, incorrect, skipped
	"""

	score = 0
	correct = {}
	incorrect = {}
	skipped = {}

	i = 0
	for wrong, right in zip(answers, key):
		i += 1
		if (wrong == right):
			score += 6
			correct[i] = right
		elif (wrong == 's'):
			score += 1.5
			skipped[i] = right
		else:
			incorrect[i] = right

	return score, correct, incorrect, skipped

def cutoff(year: int, test: str) -> int:
	"""AIME cutoff for a specific year and test

	Args:
		year (int): 2003 - 2020
		test (str): A, B

	Returns:
		int: cutoff
	"""

	cutoffs = pd.read_html('https://ivyleaguecenter.org/2016/01/23/1487/')[0]
	cutoffs = cutoffs.rename(columns=cutoffs.iloc[0])[1:]

	score = cutoffs.loc[cutoffs['Year'] == str(year), 'AMC 10' + test.upper()]

	return float(score)

with open('answers.txt') as f:
	answers = [i.strip().lower() for i in f.readlines()]

with open('info.json') as f:
	data = json.load(f)
	year = data['year']
	test = data['test'].upper()
	link = f'https://artofproblemsolving.com/wiki/index.php/{year}_AMC_10{test}_Answer_Key'

page = requests.get(link).text
extractor = Extractor.from_yaml_file('selector.yml')
key = [i.lower() for i in extractor.extract(page)['Answers']]

with open('score.txt', 'w') as f:
	score, correct, incorrect, skipped = grade(answers, key)
	f.write(summarize(score, cutoff(year, test), correct, incorrect, skipped))
