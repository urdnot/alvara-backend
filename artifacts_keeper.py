import os
import image_mixer as mixer
import json
import utils
import re


class ArtifactsKeeper:
    META_FILE_RX = re.compile("^[1-9][0-9]*.json$")
    IMAGE_FILE_RX = re.compile("^[1-9][0-9]*.png$")
    EXTERNAL_FILE_RX = re.compile("^[1-9][0-9]*.png$")

    def __init__(self, directory, settings_path):
        self.DIR = directory
        self.META_DIR = self.DIR + "meta/"
        self.IMAGE_DIR = self.DIR + "image/"
        self.EXTERNAL_DIR = self.DIR + "external/"
        self.settings = self._read_json(settings_path)
        self._add_assets_pathes()
        utils.create_dir_if_not_exist(self.DIR)
        utils.create_dir_if_not_exist(self.META_DIR)
        utils.create_dir_if_not_exist(self.IMAGE_DIR)
        utils.create_dir_if_not_exist(self.EXTERNAL_DIR)
        utils.clear_garbage(self.META_DIR, self.META_FILE_RX)
        utils.clear_garbage(self.IMAGE_DIR, self.IMAGE_FILE_RX)
        utils.clear_garbage(self.EXTERNAL_DIR, self.EXTERNAL_FILE_RX)

    def _add_assets_pathes(self):
        assets = self.settings['assets_path']
        image_prefix = str(self.settings['image'])
        external_prefix = str(self.settings['external'])
        for cat in self.settings['categories']:
            category = cat['name']
            for attr in cat['attributes']:
                attribute = attr['name']
                for op in attr['options']:
                    for pic in op['pics']:
                        pic['image'] = assets + "/" + image_prefix + "/" + category + "/" + attribute + "/" + pic['path']
                        pic['external'] = assets + "/" + external_prefix + "/" + category + "/" + attribute + "/" + pic['path']

    def _read_json(self, path):
        f = open(path, 'r')
        content = json.load(f)
        f.close()
        return content

    def token_exist(self, num):
        return os.path.exists(self.token_meta(num))

    async def create_image(self, data):
        layers = []
        for i in range(0, len(data.options)):
            for part in self.settings['categories'][data.category_id]['attributes'][i]['options'][data.options[i]]['pics']:
                layers.append({'path': part['image'], 'z': part['z']})
        return self._mix_and_save_picture(layers, self.IMAGE_DIR, self.path_to_image(data.token_id))

    def create_external(self, data):
        layers = []
        for i in range(0, len(data.options)):
            for part in self.settings['categories'][data.category_id]['attributes'][i]['options'][data.options[i]]['pics']:
                layers.append({'path': part['external'], 'z': part['z']})
        return self._mix_and_save_picture(layers, self.EXTERNAL_DIR, self.path_to_external(data.token_id))

    def _mix_and_save_picture(self, layers, workdir, result_path):
        tmp_path = workdir + utils.temp_name()
        mixer.mix(layers, tmp_path)
        utils.rename_safely(tmp_path, result_path)
        return result_path

    async def create_meta(self, token_id, content):
        result_meta_path = self.token_meta(token_id)
        tmp_path = self.META_DIR + utils.temp_name()
        with open(tmp_path, 'w') as out:
            json.dump(content, out)
        utils.rename_safely(tmp_path, result_meta_path)

    def token_meta(self, token_id):
        return self.META_DIR + str(token_id) + ".json"

    async def token_meta_content(self, token_id):
        with open(self.token_meta(token_id), 'r') as file:
            return json.load(file)

    def path_to_image(self, token_id):
        return self.IMAGE_DIR + str(token_id) + ".png"

    def image_content(self, token_id):
        with open(self.path_to_image(token_id), 'rb') as file:
            return file.read()

    def path_to_external(self, token_id):
        return self.EXTERNAL_DIR + str(token_id) + ".png"

    def external_content(self, token_id):
        with open(self.path_to_external(token_id), 'rb') as file:
            return file.read()

