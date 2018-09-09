from peewee import *
import datetime
from util import log
import util

db = SqliteDatabase('../db/bets.db')
inputdb = SqliteDatabase('../db/input.db')
betcollectdb = SqliteDatabase('../db/betcollect.db')


class DBBetInput(Model):
    txid = CharField(unique=True)
    bet_block_height = IntegerField()
    bet_amount = FloatField()
    bet_nonce_last_digit = IntegerField()
    bet_state = IntegerField()

    class Meta:
        database = inputdb


class DBBetCollect(Model):
    bet_block_height = IntegerField()
    player_count = IntegerField()
    total_amount = FloatField()
    win_player_count = IntegerField()
    lose_player_count = IntegerField()
    total_win_player_amount = FloatField()
    total_lose_player_amount = FloatField()

    class Meta:
        database = betcollectdb


class DBBet(Model):
    join_txid = CharField(unique=True)
    join_block_height = IntegerField()
    join_block_hash = CharField()
    join_block_timestamp = IntegerField()
    bet_block_height = IntegerField()
    bet_block_hash = CharField()                # after result
    bet_block_timestamp = IntegerField()           # after result
    bet_block_nonce = IntegerField()            # after result
    bet_address = CharField()
    bet_amount = FloatField()
    bet_nonce_last_digit = IntegerField()
    payment_address = CharField()
    reward_amount = FloatField(default=0.0)
    payment_state = IntegerField(default=-1)     # -1 no need to pay, 0 ready to pay, 1 paied
    payment_txid = CharField()
    bet_state = IntegerField(default=-1)        # -1 un result, 0 lose, 1 win
    
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db


def write_data_to_file(file_path, data):
    try:
        f = open(file_path,'w')
        f.write(data)
        f.close()
    except Exception as _ex:
        log('write data to file error, file: {}\ndata: {} exception: {}'.format(file_path, data, _ex))


def save_bet_data(bet_list):
    with db.atomic():
        for bet in bet_list:
            try:
                dbbet = DBBet.get(DBBet.join_txid == bet.join_txid)
            except DoesNotExist:
                dbbet = None

            if dbbet is None:
                log('Net player: {} BetDigit:{} BetAmount:{}'.format(bet.payment_address,
                                                                     bet.bet_nonce_last_digit,
                                                                     bet.bet_amount))
                DBBet.create(
                    join_txid=bet.join_txid,
                    join_block_height=bet.join_block_height,
                    join_block_hash=bet.join_block_hash,
                    join_block_timestamp=bet.join_block_timestamp,
                    bet_block_height=bet.bet_block_height,
                    bet_block_hash=bet.bet_block_hash,
                    bet_block_timestamp=bet.bet_block_timestamp,
                    bet_block_nonce=bet.bet_block_nonce,
                    bet_address=bet.bet_address,
                    bet_amount=bet.bet_amount,
                    bet_nonce_last_digit=bet.bet_nonce_last_digit,
                    payment_address=bet.payment_address
                )


def get_need_pay_dbbet_list(curr_block_height):
    """
    :param curr_block_height:
    :return: [DBBet]
    """
    bet_list = DBBet.select().where(DBBet.payment_state == 0 and curr_block_height > DBBet.bet_block_height)
    return bet_list


def get_unclosing_dbbet_dict():
    """
    :return: {bet_block_height: [DBBet],...}
    """
    unclosing_dbbet_dict = {}
    unclosing_bet_list = DBBet.select().where(DBBet.bet_state == -1)
    for dbbet in unclosing_bet_list:
        bet_block_height = dbbet.bet_block_height
        if bet_block_height in unclosing_dbbet_dict:
            unclosing_dbbet_dict[bet_block_height].append(dbbet)
        else:
            unclosing_dbbet_dict[bet_block_height] = []
            unclosing_dbbet_dict[bet_block_height].append(dbbet)
        
    return unclosing_dbbet_dict


def update_dbbet_list(dbbet_list):
    with db.atomic():
        for dbbet in dbbet_list:
            dbbet.save()


def get_bet_block_list(bet_block_height):
    bet_list = DBBet.select().where(DBBet.bet_block_height == bet_block_height)
    return bet_list


# bet_block,  bet amount, bet number,bet_state, player address, txid, datetime
def get_bet_list_view_json(bet_list):
    data = []
    for bet in bet_list:
        bet_dict = {}

        bet_dict['bet_block'] = bet.bet_block_height
        bet_dict['bet_amount'] = bet.bet_amount
        bet_dict['bet_digit'] = bet.bet_nonce_last_digit
        if bet.bet_state == -1:
            bet_dict['bet_state'] = 'None'
        elif bet.bet_state == 0:
            bet_dict['bet_state'] = 'Lose'
        elif bet.bet_state == 1:
            bet_dict['bet_state'] = 'Win'
        bet_dict['player'] = bet.payment_address
        bet_dict['txid'] = bet.join_txid
        bet_dict['join_time'] = util.timestamp2localtime(bet.join_block_timestamp)

        data.append(bet_dict)
    return util.get_format_json(data)


def init_db():

    db.connect()
    db.create_tables([DBBet])

    inputdb.connect()
    inputdb.create_tables([DBBetInput])

    betcollectdb.connect()
    betcollectdb.create_tables([DBBetCollect])


def close_db():
    db.close()
    inputdb.close()
    betcollectdb.close()