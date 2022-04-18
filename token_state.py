import asyncio
import os
import json
import re
import utils


class TokenState:
    state_file_rx = re.compile("^[1-9][0-9]*$")

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
        for i in range(0, size):
            self.locks.append(asyncio.Lock())
        self.tokens = [self.Token()] * size
        self._load_state()
        self._clear_garbage()

    def _clear_garbage(self):
        for item in os.scandir(self.dir):
            if not item.is_file():
                continue
            if not self.state_file_rx.match(item.name):
                os.remove(item.path)

    def _load_state(self):
        for i in range(1, self.size + 1):
            path = self.dir + str(i)
            if os.path.exists(path):
                with open(path) as f:
                    content = json.load(f)
                self.tokens[i].state = content['state']

    def dump_token_state(self, id, data_str):
        utils.save_safely({
            'state': self.tokens[id].state,
            'data': data_str
        }, self.dir + str(id))
