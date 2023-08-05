import hashlib

def sha512(input):   
    hash = hashlib.sha512( str( input ).encode("utf-8") ).hexdigest()
    return hash

if __name__ == '__main__':
    test = sha512('test')
    print(test)
   


