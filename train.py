import os

import PIL.Image as Image
import face_recognition

import utils
from constants import Paths, DBTYPES

RESIZE_SCALE = 0.4


class Trainer:
    def __init__(self, dbType) -> None:
        super().__init__()
        if dbType == DBTYPES.WHITELIST:
            self.imagesPath = Paths.WHITELIST_IMAGES_FOLDER
            self.encodingPath = Paths.WHITELIST_ENCODING_FILE
            self.namesPath = Paths.WHITELIST_NAMES
        else:
            self.imagesPath = Paths.BLACKLIST_IMAGES_FOLDER
            self.encodingPath = Paths.BLACKLIST_ENCODING_FILE
            self.namesPath = Paths.BLACKLIST_NAMES

    def addName(self, name):
        names = self.readNames()
        names.append(name)
        os.mkdir(self.imagesPath % name)
        utils.saveNames(self.namesPath, names)

    def removeName(self, name):
        names = self.__readNames()
        names.remove(name)
        os.rmdir(self.imagesPath % name)
        os.remove(self.encodingPath % name)
        utils.saveNames(self.namesPath, names)

    def readNames(self):
        return utils.loadNames(self.namesPath)

    def __listImages(self, name):
        return os.listdir(self.imagesPath % name)

    def __train(self, name, imageName):
        imagePath = (self.imagesPath % name) + "/" + imageName
        self.__resizeAndGrey(imagePath)
        imageF = face_recognition.load_image_file(imagePath)
        enc = face_recognition.face_encodings(imageF)
        if len(enc) >= 1:
            return enc[0]
        return []

    def trainImage(self, name, imageName):
        encodings = utils.loadEncodings(self.encodingPath % name)
        encoding = self.__train(name, imageName)
        encodings.append(encoding)
        utils.saveEncodings(self.encodingPath % name, encodings)
        if len(encoding) >= 1:
            return Trainer
        return False

    def trainPerson(self, name):
        images = self.__listImages(name)
        encodings = utils.loadEncodings(self.encodingPath % name)
        for image in images:
            encoding = self.__train(name, image)
            encodings.append(encoding)
        utils.saveEncodings(self.encodingPath % name, encoding)

    def __resizeAndGrey(self, imagePath):
        print("converting " + imagePath + " to greyscale and resize")
        img = Image.open(imagePath)
        w, h = img.size
        newImage = img.resize((int(w * RESIZE_SCALE), int(h * RESIZE_SCALE)), Image.ANTIALIAS)
        LImage = newImage.convert('L')
        LImage.save(imagePath)

    def loadDataset(self):
        names = self.readNames()
        encodings = []
        labels = []
        for name in names:
            nameEnc = utils.loadEncodings(self.encodingPath % name)
            for nameEn in nameEnc:
                encodings.append(nameEn)
                labels.append(name)
        return names, encodings
