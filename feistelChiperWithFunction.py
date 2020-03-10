from feistelFunction import FeistelFunction
import sampleText
# def xor_function(a,b):
#     return a^b

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
        for i in range(num_key):
            self.internal_key.append(key)
            
            
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
        
        