import json
import artifacts_keeper

ATTR_COUNT = 7
PACK_FIELD_BITSIZE = 5
PACK_FIELD_MASK = (1 << PACK_FIELD_BITSIZE) - 1


class GenomeData:
    def __init__(self):
        self.rerolled = False
        self.category_id = 0
        self.options = []


def _unpack_genome(str):
    num = int(str)
    result = GenomeData()

    # get reroll flag
    result.rerolled = num & 0b1
    num = num >> 1

    # get random category id
    result.category_id = (num & PACK_FIELD_MASK) / 2
    num = num >> PACK_FIELD_BITSIZE

    # get options
    result.options = [0] * ATTR_COUNT
    for i in range(0, ATTR_COUNT):
        result.options[i] = num & PACK_FIELD_MASK
        num = num >> PACK_FIELD_BITSIZE
    return result


def _category_description(category_id):
    if category_id == 1:
        description = 'The category includes 4,500 photos. It’s focused on not related to time or place everyday moments of Alvara’s life. Generally, she led a quiet, measured life at that time, so she was dressed in the typical clothes of that time and place.'
    elif category_id == 2:
        description = 'The category includes 2,500 photos. This group reveals a little more of Alvara’s feminine side. Any couturier in the Commonwealth of Planets would envy such a collection of lingerie. Alvara is said to have a separate room in her home for such clothes.'
    elif category_id == 3:
        description = 'The category consists of 2,000 photos. There were large-scale wars before and, not surprisingly, even after the war with the Iguns. Alvara has been involved in many, many wars. This category contains photos of her service as a common private soldier.'
    elif category_id == 4:
        description = 'The category contains 900 photos. Alvara was sometimes bored of being an ordinary soldier. She could demonstrate her leadership and fighting skills, which instantly brought her to the forefront of military conflict. People trusted her to take command of another elite squad to solve problems of high complexity. This kind of squad had state-of-the-art equipment.'
    elif category_id == 5:
        description = 'The category has 100 photos. To be the most powerful entity of the Commonwealth of Planets and not take full advantage of it, at least locally in some lost corner of the galaxy, no, that’s not about Alvara. There were times when she wanted to be the center of attention. To turn the tide of a lost war on her own. To find a backward planet and, like Prometheus, give them the flame of genuine knowledge. Alvara, in these photos, is like a Greek goddess of war, enlightenment, or wisdom.'
    else:
        raise Exception('Invalid category')
    return description


def _read_settings(path):
    f = open(path, 'r')
    settings = json.load(f)
    f.close()
    return settings


def _attributes_set(info, settings):
    result = {}
    cat_name = settings['categories'][info.category_id]['name']
    result.append = {
        "trait_type": "category",
        "value": cat_name
    }
    attributes = settings['categories'][info.category_id]['attributes']
    for i in range(0, len(info.options)):
        result.append = {
            "trait_type": attributes[i]['name'],
            "value": attributes[i]['options'][info.options[i]]['name']
        }
    return result


def _metadata_json(info, image_path, high_resolution_path, settings):
    return {
        'description': _category_description(info.category_id),
        'image': image_path,
        'external_url': high_resolution_path,
        'name': 'Alvara',
        'attributes': _attributes_set(info, settings)
    }


def meta(num):
    # Ask smart contract about token 'num'
    # call getData(num) of smart contract, and receive 'genome_str'
    pass