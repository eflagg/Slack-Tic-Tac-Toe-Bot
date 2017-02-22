from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
	"""Table for tictactoe games."""

	__tablename__ = "games"

	game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_1_id = db.Column(db.String(50), db.ForeignKey("users.user_id"), nullable=False)
	user_2_id = db.Column(db.String(50), db.ForeignKey("users.user_id"), nullable=True)
	board = db.Column(db.String(100), nullable=False)
	channel_id = db.Column(db.String(50), db.ForeignKey("channels.channel_id"), nullable=False)
	next_player_name = db.Column(db.String(50), nullable=False)
	is_over = db.Column(db.Boolean, nullable=True)

	channel = db.relationship("Channel", backref="games")
	user_1 = db.relationship("User", foreign_keys=[user_1_id])
	user_2 = db.relationship("User", foreign_keys=[user_2_id])


class User(db.Model):
	"""Table for users of tictactoe game."""

	__tablename__ = "users"

	user_id = db.Column(db.String(50), primary_key=True)
	name = db.Column(db.String(20), nullable=False, unique=True)
	num_wins = db.Column(db.Integer, default=0, nullable=False)


class Channel(db.Model):
	"""Table for channels tictactoe games are played."""

	__tablename__ = "channels"

	channel_id = db.Column(db.String(50), primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	num_games_played = db.Column(db.Integer, default=0, nullable=True)


def connect_to_db(app, db_uri='postgresql:///tictactoe'):
	"""Connect the database to Flask app."""

	app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
	db.app = app
	db.init_app(app)
	db.create_all()


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
