import vault

ALPHABET = "-+=/|}{'.,<?>~`0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"

class DSPM:

    def __init__(self):
        self.running = True
        self.vaultDetails = []
        #self.getConfigOptions()
        self.secretKey = "*"
        self.vaultData = []
        self.sync = -1
        #self.checkSyncStatus()
        
    """
    def getConfigOptions():
        confFile = open("dspm.conf", "r")
        for line in confFile:
            confOptions = line.split(",")
            self.vaultDetails.append(confOptions)
        self.checkSyncStatus()

    """
    
    def menu(self, args):
        if args == None:
            print("")
            print("Options: ")
            print("(1) Create a new vault")
            print("(2) Open a local vault")
            print("(3) Load a vault from online drive.")
            print("(4) Quit")
            choice = int(input("> "))
            if choice == 1:
                self.initVault()
            elif choice == 2:
                self.openVault()
            elif choice == 3:
                self.loadVaultFromDrive()
            elif choice == 4:
                self.running = False
        else:
            if args[0] == "-c" or args[0] == "create":
                self.initVault(args[1])
            elif args[0] == "-o" or args[0] == "open":
                self.openVault(args[1])

    def initVault(self, name='default'):
        if name == 'default':
            name = input("Enter a name for your vault: ")
        myVault = vault.Vault(name)
        details = myVault.getPassword()
        password = details[0]
        salt = details[1]
        cipherText = myVault.encryptKey(myVault.generateKey(), password)
        myVault.writeToFile(cipherText, salt)
        myVault.createVaultFile()
        print("Initialisation complete")

    def loadVaultFromDrive(self):
        name = input("Enter the vault name to retrieve: ")
        myVault = vault.Vault(name)
        myVault.setUpSyncing()
        myVault.getFile()

    def openVault(self, name='default'):
        if name == 'default':
            name = input("Enter the vault name to open: ")
        myVault = vault.Vault(name)
        self.secretKey = myVault.openVault()
        self.vaultData = myVault.readPasswordFile(self.secretKey)
        self.presentVaultOptions(myVault)

    def presentVaultOptions(self, myVault):
        if self.secretKey != "*":
            print("")
            print("Options:")
            print("(1) Retrieve Password")
            print("(2) New Password")
            print("(3) Remove Password")
            print("(4) List Passwords")
            print("(5) Change File Locations")
            print("(6) Sync Files")
            print("(7) Go Back to Main Menu")
        else:
            self.menu(None)
            return
        choice = int(input("> "))
        if choice == 1:
            myVault.printTitles(self.vaultData)
            index = int(input("Enter password number: "))
            myVault.readEntry(index, self.vaultData)
        elif choice == 2:
            size = int(input("Enter a password length: "))
            newPassword = myVault.generatePassword(size, ALPHABET)
            newTitle = input("Enter a title for this new password: ")
            self.vaultData.append(myVault.appendEntry(newPassword, newTitle))
            myVault.saveToFile(self.secretKey, self.vaultData)
            print("Entry created.")
        elif choice == 3:
            myVault.printTitles(self.vaultData)
            index = int(input("Enter a password number to remove: "))
            myVault.removeEntry(index, self.vaultData)
            myVault.saveToFile(self.secretKey, self.vaultData)
            print("Entry removed.")
        elif choice == 4:
            myVault.printTitles(self.vaultData)
        elif choice == 5:
            #this will move files.
            print("Move files.")
        elif choice == 6:
            if self.sync != -1:
                #syncing has been set up, use correct option
                self.syncOptions()
            else:
                myVault.setUpSyncing()
                self.syncOptions()
        elif choice == 7:
            self.menu(None)
            return
            
        self.presentVaultOptions(myVault)

    def syncOptions(self):
        print("Sync Options:")
        print("(1) Download Password File From Drive")
        print("(2) Update Password File On Drive")
        print("(3) Back to Vault Menu")
        choice = int(input("> "))
        if choice == 1:
            myVault.getFile()
        elif choice == 2:
            #myVault.uploadFile()
            print("This will update file.")
        elif choice == 3:
            self.presentVaultOptions()

    #def checkSyncStatus(self):
