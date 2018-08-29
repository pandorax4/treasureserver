def write_last_update_view_block(block_height):
    f = open(last_update_view_record_file,'w')
    f.write(str(block_height))
    f.close()


def generate_bet_block_info(bet_block_height):
    log('Try Update bet block info: {}'.format(bet_block_height))
    bet_list = datacenter.get_bet_block_list(bet_block_height)
    if len(bet_list) > 0:
        log('Generate bet block info json , bet count: {}'.format(len(bet_list)))
        json_str = datacenter.get_bet_list_view_json(bet_list)
        file_path = bet_view_path.format(bet_block_height)
        f = open(file_path,'w')
        f.write(json_str)
        f.close()


def workthread_update_view():
    global is_updating_view
    #try:
    curr_block_height = api.get_curr_blockchain_height()
    last_update_block_height = curr_block_height
    # read last update block
    if os.path.exists(last_update_view_record_file):
        f = open(last_update_view_record_file,'r')
        text = f.read()
        f.close()
        last_update_block_height = int(text)

    if last_update_block_height > curr_block_height:
        log('Something wrong, last update block height is > curr block_height: {} > {}'.format(last_update_block_height,curr_block_height))
    elif last_update_block_height < curr_block_height:
        start = last_update_block_height + 1
        end = curr_block_height + 1
        last_bet_block = model.get_bet_block_height_by_join_block_height(last_update_block_height)
        # force update last bet block, because i'm not sure last bet block info is update successfuly.
        generate_bet_block_info(last_bet_block)
        for block_height in range(start,end):
            curr_bet_block = model.get_bet_block_height_by_join_block_height(block_height)
            if curr_bet_block != last_bet_block:
                generate_bet_block_info(curr_bet_block)
                last_bet_block = curr_bet_block
            last_update_block_height = block_height
            write_last_update_view_block(last_update_block_height)
    else:
        bet_block = model.get_bet_block_height_by_join_block_height(curr_block_height)
        generate_bet_block_info(bet_block)
        write_last_update_view_block(curr_block_height)

        # Commit to page

    is_updating_view = False
    #except Exception as _e:
    #    is_updating_view = False
     #   log('Update view exception: ' + str(_e))

    
def update_view():
    global is_updating_view
    if is_updating_view == True:
        return
    is_updating_view = True
    #try:
    t = threading.Thread(target=workthread_update_view)
    t.setDaemon(True)
    t.start()
    #except:
    #    is_updating_view = False