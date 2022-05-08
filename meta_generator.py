import token_state
import threading


class MetaGenerator:
    ATTR_COUNT = 7
    PACK_FIELD_BITSIZE = 5
    PACK_FIELD_MASK = (1 << PACK_FIELD_BITSIZE) - 1
    TOKEN_NAME = "Alvara #"

    def __init__(self, keeper, state, smart, domain, image_path, external_path):
        self.keeper = keeper
        self.state = state
        self.smart = smart
        self.image_url = domain + image_path
        self.external_url = domain + external_path

    class TokenData:
        def __init__(self):
            self.token_id = -1
            self.rerolled = False
            self.category_id = -1
            self.options = None

    def _unpack_token_data(self, str, token_id):
        num = int(str)
        result = self.TokenData()
        result.token_id = token_id

        # get options
        result.options = [0] * self.ATTR_COUNT
        for i in range(0, self.ATTR_COUNT):
            result.options[i] = num & self.PACK_FIELD_MASK
            num = num >> self.PACK_FIELD_BITSIZE
        result.options.reverse()

        # get random category id
        result.category_id = (num & self.PACK_FIELD_MASK) // 2
        num = num >> self.PACK_FIELD_BITSIZE

        # get reroll flag
        result.rerolled = num & 0b1
        num = num >> 1
        return result

    def _category_description(self, category_id):
        if category_id == 0:
            description = 'The category includes 4,500 photos. It’s focused on not related to time or place everyday moments of Alvara’s life. Generally, she led a quiet, measured life at that time, so she was dressed in the typical clothes of that time and place.'
        elif category_id == 1:
            description = 'The category includes 2,500 photos. This group reveals a little more of Alvara’s feminine side. Any couturier in the Commonwealth of Planets would envy such a collection of lingerie. Alvara is said to have a separate room in her home for such clothes.'
        elif category_id == 2:
            description = 'The category consists of 2,000 photos. There were large-scale wars before and, not surprisingly, even after the war with the Iguns. Alvara has been involved in many, many wars. This category contains photos of her service as a common private soldier.'
        elif category_id == 3:
            description = 'The category contains 900 photos. Alvara was sometimes bored of being an ordinary soldier. She could demonstrate her leadership and fighting skills, which instantly brought her to the forefront of military conflict. People trusted her to take command of another elite squad to solve problems of high complexity. This kind of squad had state-of-the-art equipment.'
        elif category_id == 4:
            description = 'The category has 100 photos. To be the most powerful entity of the Commonwealth of Planets and not take full advantage of it, at least locally in some lost corner of the galaxy, no, that’s not about Alvara. There were times when she wanted to be the center of attention. To turn the tide of a lost war on her own. To find a backward planet and, like Prometheus, give them the flame of genuine knowledge. Alvara, in these photos, is like a Greek goddess of war, enlightenment, or wisdom.'
        else:
            # TODO: important to catch and process this exception
            raise Exception('Invalid category')
        return description

    def _attributes_set(self, data):
        result = []
        cat_name = self.keeper.settings['categories'][data.category_id]['name']
        result.append({
            "trait_type": "category",
            "value": cat_name
        })
        attributes = self.keeper.settings['categories'][data.category_id]['attributes']
        for i in range(0, len(data.options)):
            result.append({
                "trait_type": attributes[i]['name'],
                "value": attributes[i]['options'][data.options[i]]['name']
            })
        return result

    def _metadata_json(self, data):
        return {
            'description': self._category_description(data.category_id),
            'image': self.image_url + str(data.token_id),
            'name': self.TOKEN_NAME + str(data.token_id),
            'external_url': self.external_url + str(data.token_id),
            'attributes': self._attributes_set(data)
        }

    async def _ask_smart_for_token_data(self, num):
        return self.smart.get_token_data(num)

    async def _create_artifacts(self, data, token_id):
        await self.keeper.create_image(data)
        content = self._metadata_json(data)
        await self.keeper.create_meta(token_id, content)
        await self.state.dump_token_state(token_id)
        t = threading.Thread(target=self.keeper.create_external, args=(data,))
        t.daemon = True
        t.start()
        return content

    async def meta(self, token_id):
        content = None
        async with self.state.locks[token_id]:
            if self.state.tokens[token_id].state == token_state.TokenState.Token.NOT_EXIST:
                # Ask smart contract about token 'token_id'
                # call getData(num) of smart contract, and receive 'genome_str'
                self.state.tokens[token_id].data = await self._ask_smart_for_token_data(token_id)
                unpacked_data = self._unpack_token_data(self.state.tokens[token_id].data, token_id)
                self.state.tokens[token_id].state = token_state.TokenState.Token.NOT_REROLLED if unpacked_data.rerolled == 0 else token_state.TokenState.Token.REROLLED
                content = await self._create_artifacts(unpacked_data, token_id)

            elif self.state.tokens[token_id].state == token_state.TokenState.Token.NOT_REROLLED:
                # Ask smart contract about token 'token_id'
                # call getData(num) of smart contract, and receive 'genome_str'
                data_str = await self._ask_smart_for_token_data(token_id)
                if data_str != self.state.tokens[token_id].data:
                    self.state.tokens[token_id].data = data_str
                    data = self._unpack_token_data(data_str, token_id)
                    self.state.tokens[token_id].state = token_state.TokenState.Token.REROLLED
                    content = await self._create_artifacts(data, token_id)
                else:
                    content = await self.keeper.token_meta_content(token_id)
            elif self.state.tokens[token_id].state == token_state.TokenState.Token.REROLLED:
                content = await self.keeper.token_meta_content(token_id)
            return content
