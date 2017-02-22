from model import db
from helpers import create_board, show_board, make_move, is_board_full, find_winner
from db_helpers import get_game, get_user_by_id, get_user_by_name, add_user, is_channel, add_channel, add_game

RESPONSE_TEXTS = ["Game already in play.",
                "Must input an integer. Ex: \'/ttt move 5\'",
                "You must challenge someone before you can make a move. Ex: \'/ttt @user\'",
                "It's not your turn. Wait until the other player makes a move.",
                "Game over. Tie game. Play again!",
                "/ttt @user -- Challenge someone to a game \n/ttt move 5 -- Makes a move at position 5 \n/ttt status -- shows current board and who's next",
                "Someone has already played in this position. Try again.",
                "Please challenge a player in this channel.",
                "No one is currently playing a game. Start one!",
                "Number must be 1-9. Try again."]


def get_start_game_response(text, channel_id, channel_name, user_id, user_name):
    """Process initiation of tictactoe when a challenge is made and 
    return response text (ttt board and next player).
    """
    
    #Check if game already in session. If so, return error message.
    if get_game(channel_id):
        return (RESPONSE_TEXTS[0], None)

    #Check if users and channel are in db, if not, add them.
    user = get_user_by_id(user_id)
    if not user:
        user = add_user(user_id, user_name)
    if not is_channel(channel_id):
        add_channel(channel_id, channel_name)

    #Get user_2 name from text
    user_2_name = text[1:]


    #Instantiate new game instance with newly made board and add to db.
    board = create_board()
    game = add_game(user_id, user_2_name, board, channel_id)

    attachment_text = "It\'s %s\'s move." % game.next_player_name

    return (show_board(board), attachment_text)


def get_move_response(text, channel_id, user_id, user_name):
    """Process a move and return response text (ttt board and next player)."""
       
    #Get num from text for move position. If not a num or out of range, return error.
    try:
        position = int(text[-1])
        if position not in range(1, 10):
            return (RESPONSE_TEXTS[9], None)
    except ValueError:
        return (RESPONSE_TEXTS[1], None)

    #Check if game is in session and send error message if not.
    game = get_game(channel_id)
    if not game:
        return (RESPONSE_TEXTS[2], None)

    #Return error if not their turn.            
    if game.next_player_name != user_name:
        return (RESPONSE_TEXTS[3], None)

    #Check if user 2 is in db or current game and add if not.
    if not game.user_2_id and game.user_1_id != user_id:
        user_2 = get_user_by_id(user_id)
        if not user_2:
            user = add_user(user_id, user_name)
        game.user_2_id = user_id
        db.session.commit()

    #Set current player to X or O, depending on whose turn it is
    if user_id == game.user_1_id:
        current_player = "X"
    else:
        current_player = "O"

    #Create updated board with move. Add it to db and return it to users.
    updated_board = make_move(game.board, position, current_player)
    if updated_board:
        game.board = updated_board
        db.session.commit()
    else:
        return (show_board(game.board), RESPONSE_TEXTS[6])

    #Check if board is full or has winner. Return message if either true.
    if find_winner(updated_board):
        game.is_over = True
        db.session.commit()
        attachment_text = "Game over. %s is the winner! Play again!" % game.next_player_name
    elif is_board_full(updated_board):
        game.is_over = True
        db.session.commit()
        attachment_text = RESPONSE_TEXTS[4]
    else:
        #Update who is the next player in db and indicate in msg.
        if game.next_player_name == game.user_1.name:
            game.next_player_name = game.user_2.name
        else:
            game.next_player_name = game.user_1.name
        db.session.commit()
        attachment_text = "It\'s %s\'s move." % game.next_player_name

    return (show_board(updated_board), attachment_text)


def get_help_response():
    """Process help request and respond with possible commands."""

    return (RESPONSE_TEXTS[5], None)


def get_status_response(channel_id):
    """Process status request and respond with current board and next player."""

    game = get_game(channel_id)

    if not game:
        return (RESPONSE_TEXTS[8], None)

    else:
        attachment_text = "It\'s %s\'s move." % game.next_player_name
        return (show_board(game.board), attachment_text)