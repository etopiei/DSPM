# DSPM - Dead Simple Password Manager
This password manager is designed to be run from command line, though it may be ported to other systems later.
The idea behind it is, you get the security of all your passwords being unique and strong, while at the same time allowing you greater control over where your passwords are stored.
This utility is especially well suited to syncing passwords over google drive or one drive while keeping them secure, this can be useful when switching operating systems or environments.

Usage: At the moment functionality is limited, use run.py to open this app and follow the prompts,
or you can use command line options to do some basic operations.

	$python3 run.py open [vaultName]
	$python3 run.py -o [vaultName]
	$python3 run.py create [vaultName]
	$python3 run.py -c [vaultName]