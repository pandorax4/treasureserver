from peewee import *
import datetime
import os

db_root = "./db/"
db_name = "bets.db"

db = SqliteDatabase(db_root + db_name)

class DBBet(Model):
	join_txid = CharField(unique=True)
	join_block_height = IntegerField()
	join_block_hash = CharField()
	join_block_timestamp = IntegerField()
	bet_number = IntegerField()
	bet_address = CharField()
	bet_amount = FloatField()
	payment_address = CharField()

	bet_state = IntegerField(default=-1)  # -1 not closing, 0 lose, 1 win
	settlement_block_height = IntegerField(default=-1)
	settlement_block_hash = CharField(default="")
	settlement_block_nonce = IntegerField(default=-1)

	payment_state = IntegerField(default=-1) # -1 no need pay, 0 unpay, 1 paid
	reward_amount = FloatField(default=0.0)
	reward_txid = CharField(default="")

	update_at = DateTimeField(default=datetime.datetime.now())
	created_at = DateTimeField(default=datetime.datetime.now())

	class Meta:
		database = db


def get_unsettle_bet_list():
	unsettle_bet_list = DBBet.select().where(DBBet.bet_state == -1)
	return unsettle_bet_list


def save_new_bet_list(_bet_list):
	if _bet_list is None or len(_bet_list) == 0:
		return

	with db.atomic():
		for bet in _bet_list:
			try:
				dbbet = DBBet.get(DBBet.join_txid == bet["join_txid"])
			except DoesNotExist:
				dbbet = None

			if dbbet is None:
				print("New bet: ", bet["join_txid"], bet["bet_amount"])
				DBBet.create(
					join_txid = bet["join_txid"],
					join_block_height = bet["join_block_height"],
					join_block_hash = bet["join_block_hash"],
					join_block_timestamp = bet["join_block_timestamp"],
					bet_number = bet["bet_number"],
					bet_address = bet["bet_address"],
					bet_amount = bet["bet_amount"],
					payment_address = bet["payment_address"],
				)


def save_settlement_bet_list(_dbbet_list):
	if _dbbet_list is None or len(_dbbet_list) == 0:
		return

	with db.atomic():
		for dbbet in _dbbet_list:
			dbbet.save()


def init_db():
	if not os.path.exists(db_root):
		print("To Create database dir!")
		os.mkdir(db_root)
	db.connect()
	db.create_tables([DBBet])

def close_db():
	db.close()