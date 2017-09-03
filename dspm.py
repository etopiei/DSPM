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

    def menu(self):
        print("Welcome to DSPM - Dead Simple Password Manager")
        print("Options: ") 
        choice = int(input("(1) Create a new vault\n(2) to open vault\n(3) to quit app\n>"))
        if choice == 1:
            self.initVault()
        elif choice == 2:
            self.openVault()
        elif choice == 3:
            self.running = False

    def initVault(self):
        vaultName = input("Enter a name for your vault: ")
        myVault = vault.Vault(vaultName)
        details = myVault.getPassword()
        password = details[0]
        salt = details[1]
        cipherText = myVault.encryptKey(myVault.generateKey(), password)
        myVault.writeToFile(cipherText, salt)
        myVault.createVaultFile()
        print("Initialisation complete")

    def openVault(self):
        vaultName = input("Enter the vault name to open: ")
        myVault = vault.Vault(vaultName)
        self.secretKey = myVault.openVault()
        #if myVault.auth:
            #myVault.readPasswordList()
