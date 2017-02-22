from flask import Flask, request, session, jsonify
import os
# from helpers import create_board, show_board, make_move, is_board_full, find_winner
# from db_helpers import get_game, get_user_by_id, get_user_by_name, is_channel, add_user, add_channel, add_game
from processors import get_start_game_response, get_move_response, get_help_response, get_status_response
from model import connect_to_db

app = Flask(__name__)

app.secret_key = "SECRET"


@app.route('/', methods=["POST"])
def parse_request_and_respond():
    """Parse request from Slack and send response."""

    token = request.form.get('token', None)
    if token != "gK0OpDOtGmlggTyDqDKzcihf" or not token:
    	response_text = "This is not valid."
    # team_id = request.form.get('team_id', None)
    # team_domain = request.form.get('team_domain', None)
    channel_id = request.form.get('channel_id', None)
    channel_name = request.form.get('channel_name', None)
    user_id = request.form.get('user_id', None)
    user_name = request.form.get('user_name', None)
    text = request.form.get('text', None)
    
    if "@" in text:
        response_text, attachment_text = get_start_game_response(text, channel_id, channel_name, user_id, user_name)
    
    elif "move" in text:    
        response_text, attachment_text = get_move_response(text, channel_id, user_id, user_name)

    elif "help" in text:
        response_text, attachment_text = get_help_response()

    elif "status" in text:
        response_text, attachment_text = get_status_response(channel_id)

    else:
        response_text = "Sorry, I don't recognize this command. \
                        Type \'/ttt help\' if you need help."
        attachment_text = None

    response = {"response_type": "in_channel",
			"text": response_text, 
            "attachments": [{"text": attachment_text}]}
    
    return jsonify(response)


if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)