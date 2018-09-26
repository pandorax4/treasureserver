from peewee import *
import datetime
import os
import random

db_root = "./db/"
db_bet_name = "bets.db"
db_settled_name = "settled.db"

db = SqliteDatabase(db_root + db_bet_name)
db_settled = SqliteDatabase(db_root + db_settled_name)


class DBBetRound(Model):
    bet_round = IntegerField()
    bet_level = IntegerField()
    bet_count = IntegerField()
    winer_count = IntegerField()
    loser_count = IntegerField()
    total_bet_amount = IntegerField()
    total_reward = IntegerField()
    dev_reward = IntegerField()
    start_block = IntegerField()
    settled_block = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db_settled


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

    payment_state = IntegerField(default=-1)  # -1 no need pay, 0 unpay, 1 paid
    reward_amount = FloatField(default=0.0)
    reward_txid = CharField(default="")

    bet_level = IntegerField(default=1, index=True)  # 1 = small, 2 = big, 3 = large
    game_round = IntegerField(default=0, index=True)

    update_at = DateTimeField(default=datetime.datetime.now())
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


def _generate_test_bet_data():
    for x in range(10):
        DBBet.create(
            join_txid="{}adedfdf45s4fds".format(x),
            join_block_height=random.randint(10000,99999),
            join_block_hash="{}545a4sd5f4a5sd4f5s5df4a5s4df".format(x),
            join_block_timestamp=random.randint(10000000, 99999999),
            bet_number=random.randint(0, 9),
            bet_address="{}fdjwoerunnvasdfasdf".format(x),
            bet_amount=random.randint(1000, 100000),
            payment_address="{}fdjwonsdfasdfnvasdfasdf".format(x),
            bet_level=random.randint(1, 3)
        )


def get_unsettle_bet_list(_bet_level):
    unsettle_bet_list = DBBet.select().where(DBBet.bet_state == -1 and DBBet.bet_level == _bet_level)
    return unsettle_bet_list


def get_bet_list_by_round(_game_round):
    bet_list = DBBet.select().where(DBBet.game_round == _game_round)
    return bet_list


def save_new_bet_list(_bet_list, _bet_level):
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
                    join_txid=bet["join_txid"],
                    join_block_height=bet["join_block_height"],
                    join_block_hash=bet["join_block_hash"],
                    join_block_timestamp=bet["join_block_timestamp"],
                    bet_number=bet["bet_number"],
                    bet_address=bet["bet_address"],
                    bet_amount=bet["bet_amount"],
                    payment_address=bet["payment_address"],
                    bet_level=bet["bet_level"],
                )


def save_settlement_bet_list(_dbbet_list):
    if _dbbet_list is None or len(_dbbet_list) == 0:
        return

    with db.atomic():
        for dbbet in _dbbet_list:
            dbbet.save()


def get_last_game_round_number(_bet_level):
    result = DBBet.select(fn.Max(DBBet.game_round)).where(DBBet.bet_level == _bet_level)
    if result is None:
        return 0
    else:
        print(result.game_round)


def get_curr_unsettled_game_round(_bet_level):
    result = DBBet.select(fn.Max(DBBet.game_round)).where(DBBet.bet_level == _bet_level).scalar()
    print(result + 1)


def get_bet_count(_bet_level):
    #result =
    pass


def save_settled_header_data(_bet_round, _bet_level, _bet_count, _winer_count,
                             _loser_count, _total_bet_amount, _total_reward,
                             _dev_reward, _start_block, _settled_block):
    DBBetRound.Create(
        bet_round=_bet_round,
        bet_level=_bet_level,
        bet_count=_bet_count,
        winer_count=_winer_count,
        loser_count=_loser_count,
        total_bet_amount=_total_bet_amount,
        total_reward=_total_reward,
        dev_reward=_dev_reward,
        start_block=_start_block,
        settled_block=_settled_block
    )


def get_all_settled_header_data():
    return DBBetRound.select()


def init_db():
    if not os.path.exists(db_root):
        print("To Create database dir!")
        os.mkdir(db_root)
    db.connect()
    db.create_tables([DBBet])

    db_settled.connect()
    db_settled.create_tables([DBBetRound])


def close_db():
    db.close()


def test_query():
    # result = DBBet.select(fn.Max(DBBet.game_round))
    # print(len(result))
    # print(result[0].bet_level)

    """
    result = DBBet.select(DBBet, fn.Max(DBBet.game_round))
    print(type(result))
    print(len(result))
    print(type(result.get()))
    """

    """
    count = DBBet.select(fn.Count(DBBet.join_txid)).where(DBBet.bet_level == 5).scalar()
    print(count)
    """

    """
    sum = DBBet.select(fn.SUM(DBBet.bet_amount)).where(DBBet.bet_level == 2).scalar()
    print(sum, type(sum))
    """

    """
    lucky_players = DBBet.select().where(DBBet.bet_level == 1).order_by(DBBet.bet_amount.desc()).limit(3)
    for p in lucky_players:
        print(p.bet_amount)
    """





init_db()

test_query()