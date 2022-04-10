from os.path import exists

class ArtifactsKeeper:
    def __init__(self, artifacts_directory, settings):
        self.ARTIFACTS_DIRECTORY = artifacts_directory
        self.settings = settings

    def token_exist(self, num):
        return exists(self.ARTIFACTS_DIRECTORY + num)

    def create(self, data):
        pass


    def path_to_image(self, num):
        return self.ARTIFACTS_DIRECTORY + num


    def path_to_high_image(self, num):
        return self.ARTIFACTS_DIRECTORY + "high/" + num