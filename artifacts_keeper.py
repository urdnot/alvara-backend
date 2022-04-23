import os
import image_mixer as mixer
import json
import utils


class ArtifactsKeeper:
    def __init__(self, directory, settings_path):
        self.DIRECTORY = directory
        self.settings = self._read_json(settings_path)
        self._make_full_pathes()
        utils.create_dir_if_not_exist(directory)
        utils.create_dir_if_not_exist(directory + "/normal")
        utils.create_dir_if_not_exist(directory + "/meta")

    def _make_full_pathes(self):
        assets = self.settings['assets_path']
        for cat in self.settings['categories']:
            category = cat['name']
            for attr in cat['attributes']:
                attribute = attr['name']
                for op in attr['options']:
                    for pic in op['pics']:
                        pic['path'] = assets + "/" + category + "/" + attribute + "/" + pic['path']

    def _read_json(self, path):
        f = open(path, 'r')
        content = json.load(f)
        f.close()
        return content

    def token_exist(self, num):
        return os.path.exists(self.path_to_meta(num))

    def create_images(self, data):
        layers = []
        for i in range(0, len(data.options)):
            pics = self.settings['categories'][data.category_id]['attributes'][i]['options'][data.options[i]]['pics']
            layers.extend(pics)
        return mixer.mix(layers, self.path_to_image(data.token_id))

    def create_meta(self, token_id, content):
        with open(self.path_to_meta(token_id), 'w') as out:
            json.dump(content, out)

    def path_to_meta(self, token_id):
        return self.DIRECTORY + "meta/" + str(token_id) + ".json"

    def meta_content(self, token_id):
        with open(self.path_to_meta(token_id), 'r') as file:
            return json.load(file)

    def path_to_image(self, token_id):
        return self.DIRECTORY + "normal/" + str(token_id) + ".png"

    def image_content(self, token_id):
        with open(self.path_to_image(token_id), 'rb') as file:
            return file.read()
