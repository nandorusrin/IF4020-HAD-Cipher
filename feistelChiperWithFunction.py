from feistelFunction import FeistelFunction
import sampleText
# def xor_function(a,b):
#     return a^b


s_box = [
    '63','7c','77','7b','f2','6b','6f','c5','30','01','67','2b','fe','d7','ab','76',
    'ca','82','c9','7d','fa','59','47','f0','ad','d4','a2','af','9c','a4','72','c0',
    'b7','fd','93','26','36','3f','f7','cc','34','a5','e5','f1','71','d8','31','15',
    '04','c7','23','c3','18','96','05','9a','07','12','80','e2','eb','27','b2','75',
    '09','83','2c','1a','1b','6e','5a','a0','52','3b','d6','b3','29','e3','2f','84',
    '53','d1','00','ed','20','fc','b1','5b','6a','cb','be','39','4a','4c','58','cf',
    'd0','ef','aa','fb','43','4d','33','85','45','f9','02','7f','50','3c','9f','a8',
    '51','a3','40','8f','92','9d','38','f5','bc','b6','da','21','10','ff','f3','d2',
    'cd','0c','13','ec','5f','97','44','17','c4','a7','7e','3d','64','5d','19','73',
    '60','81','4f','dc','22','2a','90','88','46','ee','b8','14','de','5e','0b','db',
    'e0','32','3a','0a','49','06','24','5c','c2','d3','ac','62','91','95','e4','79',
    'e7','c8','37','6d','8d','d5','4e','a9','6c','56','f4','ea','65','7a','ae','08',
    'ba','78','25','2e','1c','a6','b4','c6','e8','dd','74','1f','4b','bd','8b','8a',
    '70','3e','b5','66','48','03','f6','0e','61','35','57','b9','86','c1','1d','9e',
    'e1','f8','98','11','69','d9','8e','94','9b','1e','87','e9','ce','55','28','df',
    '8c','a1','89','0d','bf','e6','42','68','41','99','2d','0f','b0','54','bb','16'
]

def xor(L,R):
    return bytearray(a^b for (a,b) in zip(L,R))

class FeistelNetwork:

    # Fungsi F dibikin jadi input...
    def __init__(self, key, f_function ,num_iteration = 8, block_size=16):
        self.block_size = block_size
        self.internal_key = []
        self.num_iteration = num_iteration
        self.generate_internal_key(key, num_iteration)
        self.f = f_function
        
        
    #GENERATE INTERNAL KEY BISA DIUBAH ATAU TERGANTUNG FUNSI F
    def generate_internal_key(self,key, num_key):
        prev_key = key
        for i in range(num_key):
            new_key = bytearray()
            for j in prev_key:
                new_key.append(int(s_box[j],16))
            self.internal_key.append(new_key)
            prev_key = new_key
            
            
    def encrypt_message(self, message):

        ciphertext = bytearray()
        # Split the message intoblocks
        
        splited_message = [message[i:i+self.block_size] for i in range(0,len(message),self.block_size)]
        

        # Padding if the last block wasnt enough padding with space.
        lastBlockLen = len(splited_message[-1])
        
        if lastBlockLen < self.block_size:
            for i in range(lastBlockLen, self.block_size):
                splited_message[-1].append(0x20)
                
                
        # Starting to Encrypt
        for block in splited_message:

            L = block[:self.block_size//2]
            R = block[self.block_size//2:]
            
            for i in range(0, self.num_iteration):


                key = self.internal_key[i]
                next_L = R
                R = self.f.feistelFunc(R,key[:8],key[8:])
                next_R = xor(L, R)

                L = next_L
                R = next_R


            ciphertext += L + R

        return ciphertext
    
    
    def decrypt_cipher(self, cipher):


        plaintext = bytearray()

        splited_cipher = [cipher[i:i+self.block_size] for i in range(0,len(cipher),self.block_size)]
        
        # Padding if the last block wasnt enough padding with space.
        lastBlockLen = len(splited_cipher[-1])
        
        if lastBlockLen < self.block_size:
            for i in range(lastBlockLen, self.block_size):
                splited_cipher[-1].append(0x20)
                
 
        for block in splited_cipher:
            L = block[0:self.block_size//2]
            R = block[self.block_size//2:]
            
            for i in range(self.num_iteration, 0, -1):
 
                
                key = self.internal_key[i-1]

                next_R = L
                L = self.f.feistelFunc(L,key[:8],key[8:])
                next_L = xor(R, L)
                
                R = next_R
                L = next_L
            

            plaintext += L+R
        
        return plaintext
        
            
if __name__ == '__main__':


    print("Fiestel CHIPER TESTING")

    function_class = FeistelFunction()

    message = bytearray(sampleText.english_text,"raw_unicode_escape")
    cipherMachine = FeistelNetwork(key=bytearray('csdfghjkrwertyuj',"raw_unicode_escape"),f_function = function_class )
    
    
    
    for i in cipherMachine.internal_key:
        print(i)
        print(len(i))
    
    print("The plain text is: ")
    print(message)
    print()

    ciphertext = cipherMachine.encrypt_message(message)
    print("The encrypted message is: ")
    print(ciphertext)
    print("==========================================================")
    plaintext = cipherMachine.decrypt_cipher(ciphertext)
    print("The decrypted message is: ")
    print(plaintext)
    print()
        
        