from random import SystemRandom
import getpass
from passlib.hash import pbkdf2_sha256
import aes

ALPHABET = "-+=/|}{'.,<?>~`0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"

class Vault:

    def __init__(self, name):
        self.vaultName = name
        self.auth = False

    def getPassword(self):
        cryptogen = SystemRandom()
        
        mySalt = ''.join(cryptogen.choice(ALPHABET) for i in range(16))
        print("Create a password (Ensure you remember this password, or passwords will not be recoverable)")
        userPass = getpass.getpass()
        userHashedPass = pbkdf2_sha256.hash(userPass, salt=str.encode(mySalt))
        return [userHashedPass, mySalt]

    def generateKey(self):
        cryptogen = SystemRandom()
        randLength = cryptogen.randrange(60,80)
        randLength += 20
        key = ''.join(cryptogen.choice(ALPHABET) for i in range(randLength))
        return key

    def encryptKey(self, key, userHashedPass):
        cipher = aes.AESCipher(userHashedPass)
        cipherText = cipher.encrypt(key)
        return cipherText

    def writeToFile(self, cipherText, salt):
        myFile = open("secret-" + self.vaultName + ".dspm", "wb")
        myFile.write(cipherText)
        myFile.close()
        
        myFile2 = open("salt-" + self.vaultName + ".dspm", "w")
        myFile2.write(salt)
        myFile2.close()

    def openVault(self):
        myFile = open("secret-" + self.vaultName + ".dspm", "rb")
        fileData = myFile.read()
        myFile.close()
        encryptedKey = fileData

        myFile2 = open("salt-" + self.vaultName + ".dspm", "r")
        fileData = myFile2.read()
        myFile2.close()
        mySalt = fileData
        
        password = getpass.getpass()
        hashedPassword = pbkdf2_sha256.hash(password, salt=str.encode(mySalt))
        cipher = aes.AESCipher(hashedPassword)
        key = cipher.decrypt(encryptedKey)
        print("Authentication success.")
        self.auth = True
        return key

    def createVaultFile(self):
        myFile = open("pw-" + self.vaultName + ".dspm", "w")
        myFile.write("")
        myFile.close()

    def readPasswordFile(self, key):
        pwFile = open("pw-" + self.vaultName + ".dspm", "r")
        fileData = pwFile.read()
        if len(fileData) < 16:
            #this is a dodgy hack, fix the aes decrypt function to use a better IV
            noData = []
            return noData
        cipher = aes.AESCipher(key)
        decryptedText = cipher.decrypt(fileData)
        decryptedData = decryptedText.split("\n")
        pwFile.close()
        return decryptedData

    def readEntry(self, index, vaultData):
        entry = vaultData[index-1].split(":")
        password = entry[1]
        print(password)

    def appendEntry(self, newPassword, newTitle):
        return str(newTitle) + ":" + str(newPassword)

    def removeEntry(self, index, vaultData):
        del vaultData[index-1]
        return vaultData

    def generatePassword(self, size, alpha):
        cryptogen = SystemRandom()
        newPassword = ''.join(cryptogen.choice(alpha) for i in range(size))
        return newPassword

    def saveToFile(self, key, vaultData):
        raw_text = ""
        for x in range(len(vaultData)-1):
            raw_text += str(vaultData[x]) + "\n"
        raw_text += str(vaultData[len(vaultData)-1])
        cipher = aes.AESCipher(key)
        dataToWrite = cipher.encrypt(raw_text)
        myFile = open("pw-" + self.vaultName + ".dspm", "wb")
        myFile.write(dataToWrite)
        myFile.close()

    #def moveFiles(self, newLocation, fileOption):
        #allow moving the files around 

    def printTitles(self, decryptedData):
        print("")
        titles = []
        for i in range(len(decryptedData)):
            title = decryptedData[i].split(":")
            titles.append(title[0])
        for x in range(len(titles)):
            print(x+1, titles[x], sep=". ")
        print("")
            