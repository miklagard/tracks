import tracker.util.chat_nlp as nlp
import tracker.util.log as log
from django.conf import settings

class Chat:
	def __init__(self, session, user_message=None):
		# Do not hide user's chatbox input by default
		if hasattr(self, 'terminate') == False:
			self.terminate = False

		if hasattr(self, 'iterate_index'):
			session['iterate_index'] = self.iterate_index

		if hasattr(self, 'set_iteration_session'):
			session_name = self.set_iteration_session[1]
			src_session_list = self.set_iteration_session[0]

			session['set_iteration_session_name'] = src_session_list

			session[session_name] = session[src_session_list][session['iterate_index']]

		self.set_answer(session, user_message)

		if user_message != None:
			log.log_conversation(session.session_key, 'user', user_message)

			if hasattr(self, 'direct_to'):
				session['next_chat_node'] = self.direct_to

			elif hasattr(self, 'direct_if_condition'):
				session['next_chat_node'] = nlp.find_chat_node(session, self.direct_if_condition, user_message)

			elif hasattr(self, 'direct_if_positive'):
				if nlp.determinate_yes_or_no(user_message):
					session['next_chat_node'] = self.direct_if_positive['yes']
				else:
					session['next_chat_node'] = self.direct_if_positive['no']

			elif hasattr(self, 'direct_if_session_iteration'):
				session['iterate_index'] += 1

				src_session_name = session['set_iteration_session_name']

				if len(session[src_session_name]) == session['iterate_index']:
					session['next_chat_node'] = self.direct_if_session_iteration["finished"]
				else:
					session['next_chat_node'] = self.direct_if_session_iteration["notfinished"]

		self.text = self.text.format(**session)

		if user_message == None:
			log.log_conversation(session.session_key, 'bot', self.text.format(**session))


	def set_answer(self, session, user_message):
		if user_message:
			if hasattr(self, 'update_answer_to_session'):
				if self.update_answer_to_session == 'number':
					user_message = str(nlp.get_numbers_in_sentence(user_message))

			answer = self.set_answer_to_session.format(**session)
			session[answer] = user_message.format(**session)
			log.log_session(session.session_key, answer, user_message.format(**session))