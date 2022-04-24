import asyncio
import os
import json
import re
import utils


class TokenState:
    STATE_FILE_RX = re.compile("^[1-9][0-9]*$")

    class Token:
        NOT_EXIST = 1
        NOT_REROLLED = 2
        REROLLED = 3

        def __init__(self):
            self.state = self.NOT_EXIST
            self.data = None

    def __init__(self, state_dir, size):
        self.dir = state_dir
        utils.create_dir_if_not_exist(self.dir)
        self.size = size
        self.locks = []
        self.tokens = []
        for i in range(0, size):
            self.locks.append(asyncio.Lock())
            self.tokens.append(self.Token())
        self._load_state()
        utils.clear_garbage(self.dir, self.STATE_FILE_RX)

    def _load_state(self):
        for i in range(0, self.size):
            path = self.dir + str(i + 1)
            if os.path.exists(path):
                with open(path) as f:
                    content = json.load(f)
                self.tokens[i].state = content['state']
                self.tokens[i].data = content['data']

    def dump_token_state(self, token_id):
        internal_id = token_id - 1
        utils.save_safely({
            'state': self.tokens[internal_id].state,
            'data': self.tokens[internal_id].data
        }, self.dir + str(token_id))
