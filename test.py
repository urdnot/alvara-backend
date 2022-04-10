import meta_generator as gen

SETTINGS_PATH = "settings.json"


def main():
    res = gen.meta(1)
    print(res)

if __name__ == '__main__':
    main()