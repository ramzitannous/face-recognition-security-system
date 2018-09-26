class Paths:
    PROJECT_PATH = "/home/ramzi/Desktop/Face Recognition/"
    WHITELIST_NAMES = PROJECT_PATH + "dataset/whitelist.csv"
    BLACKLIST_NAMES = PROJECT_PATH + "dataset/blacklist.csv"
    WHITELIST_ENCODING_FILE = PROJECT_PATH + "dataset/encodings/whitelist/%s.csv"
    BLACKLIST_ENCODING_FILE = PROJECT_PATH + "dataset/encodings/blacklist/%s.csv"
    WHITELIST_IMAGES_FOLDER = PROJECT_PATH + "dataset/images/whitelist/%s"
    BLACKLIST_IMAGES_FOLDER = PROJECT_PATH + "dataset/images/blacklist/%s"


class DBTYPES:
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"