# that is the file where I used a hashing function for password
# the frst thing is to install passlib

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class Hasher:

    #the function get the password from user and hashes by bcrypt function from passlib
    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)
    
    # the function takes password from user and the hashpassword
    # return true if they are == and false otherwise
    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)