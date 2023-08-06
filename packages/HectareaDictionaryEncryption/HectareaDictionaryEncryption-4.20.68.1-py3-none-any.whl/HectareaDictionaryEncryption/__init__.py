from ast import Pass


def Encrypt(message, iv, password, dictionary):

    EncryptedString = ""
    
    for nm in range(len(message)):
     
        ByteValue = message[nm]
     
        PasswordAtCurrentPosition = password[nm%len(password)]

        ProcessedValue = ( ByteValue + ( PasswordAtCurrentPosition*int.from_bytes(iv, 'big' )) ) % 256
     
        EncryptedString += dictionary[ProcessedValue]+" "

    return EncryptedString





def Decrypt(encryptedMessage, iv, password, dictionary):

    DecryptedString = b''

    encryptedMessage = encryptedMessage.split(" ")

    for nm in range(len(encryptedMessage)):

        if len(encryptedMessage[nm]) != 0:

            PasswordAtCurrentPosition = password[nm%len(password)]
            
            ValueFromDictionary = dictionary.index(encryptedMessage[nm])

            DecryptedByteValue = (ValueFromDictionary - ( PasswordAtCurrentPosition*int.from_bytes(iv, 'big' ) ) ) % 256
            
            DecryptedString += (bytes([DecryptedByteValue]))

    return DecryptedString


