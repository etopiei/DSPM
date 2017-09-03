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
        print(key)
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
        myFile = open("pw-" + self.vaultName + ".dpsm", "w")
        myFile.write("")
        myFile.close()

    def readPasswordList(self, key):
        pwFile = open("pw-" + self.vaultName + ".dspm", "r")
        titles = []
        for line in pwFile:
            fileData = line.split(":")
            titles.append(fileData[0])
        for x in range(titles):
            print(x+1, titles[x], sep=". ")

    #def readEntry(self, index):

    #def appendEntry(self, newPassword, newTitle):

    #def removeEntry(self, index):

    #def generatePassword(self, size, alpha):

    #def setUpSync(self, syncOption)


            
