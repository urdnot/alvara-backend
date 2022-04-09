import meta_generator as gen

SETTINGS_PATH = "settings.json"


def main():
    st = gen._settings(SETTINGS_PATH)
    print(st)


if __name__ == '__main__':
    main()