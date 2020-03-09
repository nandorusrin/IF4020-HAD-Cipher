



# 8-byte length left_key, right_key and input length
# Return 8-byte string
def feistelFunc(block, left_key, right_key):



    for _ in range(len(block)):

        # Cascading XOR
        for i in range(1,len(block)):
            block[i] = block[i-1]^block[i]
    
        # Do row addition and wrapping shift
        for i in range(0,8):
            block[i] = (block[i] + right_key[i])% 256


            stride = right_key[i]%8
            # create array of bits
            mask = 0xFF >> (8-stride)
            temp = (block[i]&mask) << (8-stride)
            block[i] = (block[i] >> stride) + temp
        
        # Switch row
        temp = block[0]
        for i in range(1,len(block)):
            block[i-1] = block[i]
        block[len(block)-1] = temp


def inverseFeistelFunc(block, left_key, right_key) :


    for _ in range(len(block)):

        # Switch row
        temp = block[len(block)-1]
        for row in range(len(block)-1,0,-1):
            block[row] = block[row-1]
        block[0] = temp

        # Do row addition and wrapping shift
        for row in range(0,8):

            # shift
            stride = 8 - (right_key[row]%8)
            mask = 0xFF >> (8-stride)
            temp = (block[row]&mask) << (8-stride)
            block[row] = (block[row] >> stride) + temp
            block[row] = (block[row]-right_key[row]) % 256

        # Cascading XOR
        old_value = [0 for i in range(0,len(block))]
        old_value[0] = block[0]
        for i in range(1,len(block)):
            old_value[i] = block[i]
            block[i] = block[i]^old_value[i-1]


def main():

    block = bytearray("12345669","ascii")
    right_key = bytearray("12345678","ascii")
    left_key = bytearray("12345678","ascii")

    while (len(block)!=8) or (len(right_key)!=8) or (len(left_key)!=8) :
        print("Input all must be 8 characters")
        block = input("Input block : ")
        right_key = input("Input right key : ")
        left_key = input("Input left key : ")

    feistelFunc(block, left_key, right_key)

    print(block)
    print("===================")
    inverseFeistelFunc(block, left_key, right_key)

    print(block)


main()