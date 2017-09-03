#test aes class

import aes

myCipher = aes.AESCipher("hi")
print(myCipher.key)
myCipher2 = aes.AESCipher("hi")
print(myCipher.key)

test = myCipher.encrypt("banana")
result = myCipher.decrypt(test)
print(result)

from passlib.hash import pbkdf2_sha256

userPass = "testing"

firstHash = pbkdf2_sha256.hash(userPass, salt=str.encode("5pc7sn4jdksm4cj3"))
secondHash = pbkdf2_sha256.hash(userPass, salt=str.encode("5pc7sn4jdksm4cj3"))

print(firstHash)
print(secondHash)
