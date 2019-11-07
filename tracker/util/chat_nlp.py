from django.conf import settings
import os

def find_chat_node(session, conditions, answer):
	for condition in conditions:
		conditions_file = open(os.path.join(settings.NLP_CONDITIONS_FILE, condition + '.txt'), 'r')
		conditions_data = conditions_file.read().split('\n')
		conditions_file.close()

		if ([word for word in conditions_data if (word in answer)]):
			return conditions[condition]

	return session['chat_node']
