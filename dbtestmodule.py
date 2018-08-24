
from peewee import *
import datetime
import random
import time
import json

db = SqliteDatabase('bets.db')

class Bet(Model):
    txid = CharField()
    block_hash = CharField()
    block_height = IntegerField()
    bet_block_height = IntegerField()
    bet_block_number = FixedCharField(max_length=1)
    timestamp = IntegerField()
    closing = BooleanField()
    operate_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

db.connect()
db.create_tables([Bet])

play_txid='ff7bd470351e621771f911d944f5a0a7aa25775dc0054201ff526911d212ccfa'
play_block_hash = '00000000007fb47d226df48b0c8e1d86a7977493c158a5327d3ceb9b3b73c9a3'
play_block_height = 124002
play_bet_block_height = 180000
play_bet_block_number = '4'

random_str = "abcdefghijklmnopqrstuvwxyz0123456789"
nonce_number = '0123456789'


def bet_2_json_dict(bet):
    o = {
        'txid':bet.txid,
        'block_hash':bet.block_hash,
        'block_height':bet.block_height,
        'bet_block_height':bet.bet_block_height,
        'bet_block_number':bet.bet_block_number,
        'timestamp':bet.timestamp,
        'closeing':bet.closing
    }
    return o
    #return json.dumps(o,indent=4, separators=(',',':'))




def create_bet(join_txid,join_block_hash,join_block_height,bet_block_height,bet_nonce_number, bet_timestamp,closing):
    '''
    abet = Bet.create( txid = join_txid,
                    block_hash = join_block_hash,
                    block_height = join_block_height,
                    bet_block_height = bet_block_height,
                    bet_block_number = bet_nonce_number,
                    timestamp = bet_timestamp,
                    closing = closing)
    '''
    abet = Bet()
    abet.txid = join_txid
    abet.block_hash = join_block_hash
    abet.block_height = join_block_height
    abet.bet_block_height = bet_block_height
    abet.bet_block_number = bet_nonce_number
    abet.timestamp = bet_timestamp
    abet.closing = closing

    return abet



def create_random_json():
    data = []
    for x in range(0,10000):
        join_txid = play_txid
        join_block = play_block_hash
        change_index = random.randint(0,len(join_txid) - 1)
        tmp_join_txid = list(join_txid)
        tmp_join_txid[change_index] = random.choice(random_str)
        join_txid = ''.join(tmp_join_txid)
        
        change_index = random.randint(0,len(join_block) - 1)
        tmp_join_block = list(join_block)
        tmp_join_block[change_index] = random.choice(random_str)
        join_block = ''.join(tmp_join_block)
        join_block_height = random.randint(100000,180000)
        bet_block_height = random.randint(180000,200000)
        bet_block_number = random.choice(nonce_number)
        bet_timestamp = random.randint(1533638266,1633638266)
        if random.randint(0,9) < 5:
            closing = True
        else:
            closing = False
        abet = create_bet(join_txid,join_block,join_block_height,bet_block_height,bet_block_number, bet_timestamp, closing)
        json_dict = bet_2_json_dict(abet)
        data.append(json_dict)
    
    start_time = time.time()
    json_str = json.dumps(data, indent=4, separators=(',',':'))
    f = open('data.txt','w')
    f.write(json_str)
    f.close()
    end_time = time.time()
    print('used: ', (end_time - start_time))


create_random_json()








'''
    try:
        abet = Bet.get(Bet.txid == join_txid)
        return False
    except DoesNotExist:
        abet = Bet.create( txid = join_txid,
                    block_hash = join_block_hash,
                    block_height = join_block_height,
                    bet_block_height = bet_block_height,
                    bet_block_number = bet_nonce_number,
                    timestamp = bet_timestamp)
        #abet.save()
'''
    #return True

'''
def create_random_data():
    with db.atomic(): 
        for x in range(0,10000):
            join_txid = play_txid
            join_block = play_block_hash
            change_index = random.randint(0,len(join_txid) - 1)
            tmp_join_txid = list(join_txid)
            tmp_join_txid[change_index] = random.choice(random_str)
            join_txid = ''.join(tmp_join_txid)
            
            change_index = random.randint(0,len(join_block) - 1)
            tmp_join_block = list(join_block)
            tmp_join_block[change_index] = random.choice(random_str)
            join_block = ''.join(tmp_join_block)
            join_block_height = random.randint(100000,180000)
            bet_block_height = random.randint(180000,200000)
            bet_block_number = random.choice(nonce_number)
            bet_timestamp = random.randint(1533638266,1633638266)
            if random.randint(0,9) < 5:
                closing = True
            else:
                closing = False
            if create_bet(join_txid,join_block,join_block_height,bet_block_height,bet_block_number, bet_timestamp, closing):
                print(x,'Create bet OK: ',join_txid)
            else:
                print(x,'Bet already exist: ',join_txid)

#db.close()
start_time = time.time()
create_random_data()
end_time = time.time()
print('used: ',(end_time - start_time))
'''



'''
start_time = time.time()
unclosingbets = Bet.select().where(Bet.closing == False)
end_time = time.time()
print('Count: ', len(unclosingbets))
print('used: ',(end_time - start_time))

with db.atomic():
    for bet in unclosingbets:
        bet.closing = True
        bet.save()
        print(bet.txid,bet.closing)

'''



'''
try:
    abet = Bet.get(Bet.txid == play_txid)
except DoesNotExist:
    abet = None

if abet != None:
    print('Found bet with txid:{}'.format(play_txid))
    #print('Bet number is {}'.format(abet.bet_block_number))
    #print('Change Bet Number to 9.')
    #abet.bet_block_number = '9'
    #abet.save()
    print('Bet closing state is: {}'.format(abet.closing))
    if abet.closing == False:
        print('Closing the bet.')
        abet.closing = True
        abet.save()
    abet.delete_instance()
else:
    print('Not Found a bet with txid: {}\nCreate new one.'.format(play_txid))
    abet = Bet( txid=play_txid,
                block_hash = play_block_hash,
                block_height = play_block_height,
                bet_block_height = play_bet_block_height,
                bet_block_number = play_bet_block_number, 
                timestamp=1533638266)
    abet.save()
'''