import vault

ALPHABET = "-+=/|}{'.,<?>~`0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"

class DSPM:

    def __init__(self):
        self.running = True
        #load config from file
        confFile = open("dspm.conf", "r")
        self.vaultDetails = []
        for line in confFile:
            confOptions = line.split(",")
            self.vaultDetails.append(confOptions)
        self.secretKey = "*"
        self.vaultData = []

    def menu(self, args):
        if args == None:
            print("")
            print("Options: ") 
            choice = int(input("(1) Create a new vault\n(2) to open vault\n(3) to quit app\n>"))
            if choice == 1:
                self.initVault()
            elif choice == 2:
                self.openVault()
            elif choice == 3:
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
            print("(6) Go Back to Main Menu")
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
            self.menu(None)
            return
            
        self.presentVaultOptions(myVault)
