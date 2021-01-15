function load() {
	create_input();

	var form = document.querySelector('#answers');
	form.onsubmit = submit;
}

function create_input() {
	var list = document.getElementById('answer-list');

	for (let i = 1; i <= 25; i++) {
		var element = document.createElement('li');

		var label = document.createElement('label')
		var input = document.createElement('input')

		label.setAttribute('for', i);
		input.setAttribute('class', 'answer-group');

		element.appendChild(label);
		element.appendChild(input);

		list.appendChild(element);
	}
}

function submit() {
	var form = document.querySelector('#answers');
	var answers = [];
	for (let i = 0; i < 25; i++) {
		answers.push(form.elements[i].value);
	}

	if (validate(answers)) {
		const request = new XMLHttpRequest();
		request.open('POST', '/score')

		const data = new FormData();
		data.append('answers', answers);
		request.send(data);
	}

	return true;
}
function validate(answers) { // TODO: make sure answers contain correct letters
	return true;
}
