const SENDER_AVATAR = "sender.png";
const BOT_AVATAR = "tracks.png";
const FAILED = "Could not connect API server, please retry again.";

function add_bot_message(message) {
	var content = `
	 	<div class="d-flex chat-item justify-content-end mb-4">
			<div class="msg_cotainer">
				${message}
			</div>
			<div class="img_cont_msg">
				<img src="/static/vendors/tracker/img/${BOT_AVATAR}" class="rounded-circle user_img_msg">
			</div>
		</div>
	`;

	$("#chat-area").append(content);

	scroll_to_bottom_of_chatbox();
};

function add_sender_message(message) {
	var content = `
	 	<div class="d-flex chat-item justify-content-start mb-4">
			<div class="img_cont_msg">
				<img src="/static/vendors/tracker/img/${SENDER_AVATAR}" class="rounded-circle user_img_msg">
			</div>
			<div class="msg_cotainer_send">
				${message}
			</div>
		</div>
	`;

	$("#chat-area").append(content);

	scroll_to_bottom_of_chatbox();
};

function scroll_to_bottom_of_chatbox() {
	var height = $("#chat-area").get(0).scrollHeight;

	$("#chat-area").animate({"scrollTop": height});
};

function send_message_to_api(message) {
	$.ajax({
		"url": "/api/v1/respond",
		"data": {"message": message },
		"type": "post",
		"error": function() {
			add_bot_message(FAILED);
		},
		"success": function(respond) {
			add_bot_message(respond["message"]);

			if (respond["terminate"]) {
				$("footer input, footer button").attr("disabled", true);
			}
		}
	})
}

$(document).ready(function() {
	send_message_to_api(); // Initialize
	$("#message-box").focus();

}).on("submit", "#frm-message", function(event) {
	var message = $("#message-box").val();
	event.preventDefault();
	add_sender_message(message, true);

	$("#message-box").val("").focus();

	send_message_to_api(message);
});



