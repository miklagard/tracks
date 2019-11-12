import tracker.util.chat_nlp as nlp
import tracker.util.log as log
import nltk.chat.util as nltk_chat
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
			validation_status = self.check_validated(session, user_message)

			if validation_status['validated'] == False:
				session['validation_text'] = validation_status['message'].format(**session)
			else:
				log.log_conversation(session.session_key, 'user', user_message)

				if hasattr(self, 'direct_to'):
					session['next_chat_node'] = self.direct_to

				elif hasattr(self, 'direct_if_condition'):
					session['next_chat_node'] = nlp.find_chat_node(
						self.direct_if_condition,
						self.get_message(session, user_message)
					)

				elif hasattr(self, 'direct_if_positive'):
					session['next_chat_node'] = self.direct_if_positive[
						nlp.determinate_yes_or_no(user_message)
					]

				elif hasattr(self, 'direct_if_session_iteration'):
					session['iterate_index'] += 1

					src_session_name = session['set_iteration_session_name']

					if len(session[src_session_name]) == session['iterate_index']:
						session['next_chat_node'] = self.direct_if_session_iteration["finished"]
					else:
						session['next_chat_node'] = self.direct_if_session_iteration["notfinished"]
		else: 
			if 'validation_text' in session:
				self.text = session['validation_text'].format(**session)
				del session['validation_text']
			else:
				self.text = self.text.format(**session)

			log.log_conversation(session.session_key, 'bot', self.text.format(**session))


	def user_message_cases(self, user_message):
		pairs = [
			[ '(.*), or no (.*)s actually (.*)', ['%3'] ],
			[ '(.*), sorry not (.*)', ['%3'] ],
			[ 'my name is (.*)', ['%1'] ],
			[ 'i am (.*)', ['%1'] ],
			[ 'i\'m (.*)', ['%1'] ],
			[ 'my name is (.*), (.*)', ['%1'] ],
			[ 'i am (.*), (.*)', ['%1'] ],
			[ 'i\'m (.*), (.*)', ['%1'] ],
		]

		chat = nltk_chat.Chat(pairs, nltk_chat.reflections)

		respond = chat.respond(user_message)

		if respond:
			return respond
		else:
			return user_message


	def check_validated(self, session, user_message):
		if hasattr(self, 'validate'):
			user_message = self.get_message(session, user_message)

			for case in self.validate:
				condition = case['condition']
				value = int(case['value'])
				message = case['message']

				if condition == 'greater':
					if int(user_message) > value:
						return {
							'validated': False,
							'message': message
						}
				elif condition == 'lower':
					if int(user_message) < value:
						return {
							'validated': False,
							'message': message
						}

		return {
			'validated': True
		}


	def get_message(self, session, user_message):
		if hasattr(self, 'update_answer_to_session'):
			if self.update_answer_to_session == 'number':
				user_message = str(nlp.get_numbers_in_sentence(user_message))

		return user_message


	def set_answer(self, session, user_message):
		if user_message:
			user_message = self.get_message(session, user_message)
			user_message = self.user_message_cases(user_message)

			answer = self.set_answer_to_session.format(**session)
			session[answer] = user_message.format(**session)
			log.log_session(session.session_key, answer, user_message.format(**session))