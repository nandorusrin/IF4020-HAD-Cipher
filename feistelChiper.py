
# def xor_function(a,b):
#     return a^b

def string_xor(s1,s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

class FeistelNetwork:
    # Fungsi F dibikin jadi input...
    def __init__(self, key, f_function = string_xor,num_iteration = 8, block_size=8):
        self.block_size = block_size
        self.internal_key = []
        self.num_iteration = num_iteration
        self.generate_internal_key(key, num_iteration)
        self.f = f_function
        
        
    #GENERATE INTERNAL KEY BISA DIUBAH ATAU TERGANTUNG FUNSI F
    def generate_internal_key(self,key, num_key):
        for i in range(num_key):
            self.internal_key.append('aaaa')
            
            
    def encrypt_message(self, message):
        ciphertext=""
        # Split the message intoblocks
        
        splited_message = [message[i:i+self.block_size] for i in range(0,len(message),self.block_size)]
        
        # Padding if the last block wasnt enough padding with space.
        lastBlockLen = len(splited_message[-1])
        
        if lastBlockLen < self.block_size:
            for i in range(lastBlockLen, self.block_size):
                splited_message[-1] += ' '
                
                
        # Starting to Encrypt
        for block in splited_message:
            L = block[0:self.block_size//2]
            R = block[self.block_size//2:]
            
            
            for i in range(1, self.num_iteration+1):
                key = self.internal_key[i-1]
                next_L = R
                next_R = string_xor(L, self.f(R, key)) #bisa diubah tergatung sama fungsi F nya
                
                L = next_L
                R = next_R
                
            ciphertext += L + R
        return ciphertext
    
    
    def decrypt_cipher(self, cipher):
        plaintext = ""
        
        splited_cipher = [cipher[i:i+self.block_size] for i in range(0,len(cipher),self.block_size)]
        
        # Padding if the last block wasnt enough padding with space.
        lastBlockLen = len(splited_cipher[-1])
        
        if lastBlockLen < self.block_size:
            for i in range(lastBlockLen, self.block_size):
                splited_cipher[-1] += ' '
                
 
        for block in splited_cipher:
            L = block[0:self.block_size//2]
            R = block[self.block_size//2:]
            
            for i in range(self.num_iteration, 0, -1):
                key = self.internal_key[-1]
                next_R = L
                next_L = string_xor(R, self.f(L,key))
                
                R = next_R
                L = next_L
            
            plaintext += L+R
        
        return plaintext
        
        
        

        
if __name__ == '__main__':
    print("Fiestel CHIPER TESTING")

    message = "THIS MESSAGE WILL BE ENCRYPTED"
    cipherMachine = FeistelNetwork(key='aaaa')
    
    
    print("The plain text is: ")
    print(message)
    print()

    ciphertext = cipherMachine.encrypt_message(message)
    print("The encrypted message is: ")
    print(ciphertext)
    print()
    plaintext = cipherMachine.decrypt_cipher(ciphertext)
    print("The decrypted message is: ")
    print(plaintext)
    print()
        
        