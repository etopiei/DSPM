from random import SystemRandom
import getpass
from passlib.hash import pbkdf2_sha256
import aes #requires pip install pycrypto
import googleDrive

ALPHABET = "-+=/|}{'.,<?>~`0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"

class Vault:

    def __init__(self, name):
    
        if name == None:
            newName = input("Enter vault name: ")
            self.vaultName = newName
        else:
            self.vaultName = name
            
        self.auth = False
        self.drive = None

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
        myFile.write(str.encode(salt))
        myFile.write('\n'.encode('utf-8'))
        myFile.write(cipherText)
        myFile.close()

    def openVault(self):
        myFile = open("secret-" + self.vaultName + ".dspm", "rb")
        fileData = myFile.read()
        myFile.close()
        data = fileData.split("\n".encode('utf-8'))
        mySalt = (data[0]).decode('utf-8')
        encryptedKey = data[1]
                        
        password = getpass.getpass()
        hashedPassword = pbkdf2_sha256.hash(password, salt=str.encode(mySalt))
        cipher = aes.AESCipher(hashedPassword)
        key = cipher.decrypt(encryptedKey)
        print("Vault opened.")
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

    def getFile(self):
        if self.drive == None:
            self.drive = googleDrive.GoogleDrive()
        self.drive.setFileID(self.vaultName)
        self.drive.getPasswordFileFromDrive(self.vaultName)

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
        
    def setUpSyncing(self):
        choice = input("This may open up a browser window to authenticate with google drive.\n Is this ok? (y/n)")
        if choice == "y":
            self.drive = googleDrive.GoogleDrive()
            print("Drive Account Authenticated.")

    def updateDriveFile(self):
        self.drive.setFileID(self.vaultName)
        self.drive.syncWithDrive(self.vaultName)

    def deleteDriveFile(self):
        self.drive.setFileID(self.vaultName)
        self.drive.deleteFile(self.vaultName)
        