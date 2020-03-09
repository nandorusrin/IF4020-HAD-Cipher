# 8-byte length left_key, right_key and input length
# Return 8-byte string
def feistelFunc(block, left_key, right_key):



    for _ in range(len(block)):

        # Cascading XOR
        for i in range(1,len(block)):
            block[i] = block[i-1]^block[i]
    
        # Do row addition and wrapping shift
        for i in range(0,len(block)):
            block[i] = (block[i] + right_key[i])% 256


            stride = right_key[i]%8
            mask = 0xFF >> (8-stride)
            temp = (block[i]&mask) << (8-stride)
            block[i] = (block[i] >> stride) + temp

        # Do column confusion
        array_of_bits = []
        for row in range(0,len(block)):
            array_of_bits.append([bool((0x80 >> i)&block[row]) for i in range(0,8)])

        

        # Column confusion
        # For each column in 
        for column in range(0,len(block)):
            # Get value of column
            col_value = 0
            for row in range(0,len(block)):
                col_value = col_value + (array_of_bits[row][column]<< (len(block)-1-row))
            
            # col value should be :
            col_value = (col_value + left_key[column])%256

            # Redistribute value
            for row in range(0,len(block)) :
                array_of_bits[row][column] = bool(col_value >> (len(block)-1))

        
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


        # Reverse column confusion
        array_of_bits = []
        for row in range(0,len(block)):
            array_of_bits.append([bool((0x80 >> i)&block[row]) for i in range(0,8)])


        # Column confusion
        # For each column in 
        for column in range(0,len(block)):
            # Get value of column
            col_value = 0
            for row in range(0,len(block)):
                col_value = col_value + (array_of_bits[row][column]<< (len(block)-1-row))
            
            # col value should be :
            col_value = (col_value - left_key[column])%256

            # Redistribute value
            for row in range(0,len(block)) :
                array_of_bits[row][column] = bool(col_value >> (len(block)-1))


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

    block = bytearray("12345679","ascii")
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