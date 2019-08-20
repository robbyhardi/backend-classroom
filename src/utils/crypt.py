az = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
      's','t','u','v','w','x','y','z', '0', '1', '2', '3', '4', '5', '6', '7',
      '8', '9']
def encrypt(s, text):
    res_en = ''
    for char in text:
        if char in az:
            indexOld = az.index(char)
            indexNew = (indexOld + s) % len(az)
            charNew = az[indexNew]
            res_en += charNew
        else:
            res_en += ' '
    return res_en

def decrypt(s, text):
    res_dec = ''
    for char in text:
        if char in az:
            indexOld = az.index(char)
            indexNew = (indexOld - s) % len(az)
            charNew = az[indexNew]
            res_dec += charNew
        else:
            res_dec += ' '
    return res_dec