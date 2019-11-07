from django.views.generic import View
from django.http import JsonResponse
from api.utils import get_chatbot_respond

class respond(View):
	def post(self, request):
		# Start session if it does not exist
		if not request.session.session_key:
			request.session.create()

		user_message = request.POST.get('message', '')

		bot_message = get_chatbot_respond(user_message, request.session)		

		return JsonResponse(bot_message, safe=False)

