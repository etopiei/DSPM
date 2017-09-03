import vault

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

    def menu(self, args):
        print("Welcome to DSPM - Dead Simple Password Manager")
        if args == None:
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
        #if myVault.auth:
            #myVault.readPasswordList()
