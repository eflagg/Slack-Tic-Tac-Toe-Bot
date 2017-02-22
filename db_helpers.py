from model import connect_to_db, db, Game, User, Channel

def get_game(channel_id):
    """Given a channel id, return the game object if there's one in play."""

    return db.session.query(Game).filter_by(channel_id=channel_id, is_over=False).first()


def get_user_by_id(user_id):
    """Given a user id, return the user object from the User table."""

    return db.session.query(User).filter_by(user_id=user_id).first()


def get_user_by_name(user_name):
    """Given a user name, return the user object from the User table."""

    return db.session.query(User).filter_by(name=user_name).first()


def is_channel(channel_id):
    """Given a channel id, return True if channel is in Channel table in db."""

    return Channel.query.filter_by(channel_id=channel_id).first()


def add_user(user_id, user_name):
    """Add a new user to User table in database."""

    user = User(user_id=user_id, name=user_name)
    db.session.add(user)
    db.session.commit()


def add_channel(channel_id, channel_name):
    """Add a new channel to Channel table in database."""

    channel = Channel(channel_id=channel_id, name=channel_name)
    db.session.add(channel)
    db.session.commit()


def add_game(user_id, user_2_name, board, channel_id):
    """Add a new game to Game table in database."""

    game = Game(user_1_id=user_id, next_player_name=user_2_name, board=board, channel_id=channel_id, is_over=False)
    db.session.add(game)
    db.session.commit()

    return game