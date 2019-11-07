import os
from django.conf import settings

def log_session(session_id, session_name, session_value):
	filename = os.path.join(settings.LOG_DIR, '{}.summary.log'.format(session_id))

	file = open(filename, 'a+')
	file.write('{}: {}\n'.format(session_name, session_value))
	file.close()


def log_conversation(session_id, sender, message):
	filename = os.path.join(settings.LOG_DIR, '{}.full.log'.format(session_id))

	file = open(filename, 'a+')
	file.write('{}: {}\n'.format(sender, message))
	file.close()
