import bcrypt


def hashpwd(password):
    """
    :param password: password as a string
    :return: hashed string of the password
    """

    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode()


def checkpwd(password, bcrypt_hash):
    """
    :param password: inputted password of the user
    :param bcrypt_hash: the hashed password of the user's password in the database
    :return: True if both equal each other. False if they do not.
    """

    return bcrypt.checkpw(str.encode(password), str.encode(bcrypt_hash))