def rowConfusion(block, right_key) :

    for i in range(0,len(block)) :
        block[i] = (block[i] + right_key[i])%256
        
        stride = right_key[i]%8
        mask = 0xFF >> (8-stride)
        temp = (block[i]&mask) << (8-stride)
        block[i] = (block[i] >> stride) + temp

def inverseRowConfusion(block, right_key) :
    
    
    for row in range(0,8):

        # shift
        stride = 8 - (right_key[row]%8)
        mask = 0xFF >> (8-stride)
        temp = (block[row]&mask) << (8-stride)
        block[row] = (block[row] >> stride) + temp
        block[row] = (block[row]-right_key[row]) % 256

def columnConfusion(block, left_key) :

    for col in range(0,1):

        # Get column value
        col_value = 0
        mask = 0x1<<(7-col)
        for row in range(0,len(block)) :
            XORed_value = mask&block[row]
            temp_value = XORed_value>>(7-col)
            col_value = col_value + (temp_value<<(7-row))

        # Addition

        col_value = (col_value + left_key[col])%256


        # wrapping shift
        stride = left_key[col]%8
        mask = 0xFF >> (8-stride)
        temp = (col_value&mask) << (8-stride)
        col_value = (col_value >> stride) + temp


        # Redistribute

        # Lower 1s
        mask = 0xFF>>(col+1)

        # Upper 1s
        mask += (0xFF << (len(block)-col))&0xFF

        for row in range(0,len(block)) :
            block[row] = block[row]&mask
            bit_value = ((col_value<<row)&0x80)>>col
            block[row] = block[row] + (bit_value)

def inverseColumnConfusion(block, left_key) : 
    
    for col in range(0,1):
        # Get column value
        col_value = 0
        mask = 0x1<<(7-col)
        for row in range(0,len(block)) :

            # Get block[row][col bit], put in XORed
            XORed_value = mask & block[row]

            # Shift, so value equals one (0x01)
            temp_value = XORed_value>>(7-col)
            col_value = col_value + (temp_value<<(7-row))

        # wrapping shift
        stride = 8 - left_key[col]%8
        mask = 0xFF >> (8-stride)
        temp = (col_value&mask) << (8-stride)
        col_value = (col_value >> stride) + temp

        col_value = (col_value + 256 - left_key[col])%256


        # Redistribute
        mask = 0xFF>>(col+1)
        mask += (0xFF << (len(block)-col))&0xFF
        for row in range(0,len(block)) :
            block[row] = block[row]&mask
            bit_value = ((col_value<<row)&0x80)>>col
            block[row] = block[row] + (bit_value)

def cascadingXOR(block) :
    for row in range(1,len(block)) :
        block[row] = block[row-1]^block[row]

def inverseCascadingXOR(block) :
    old_value = [0 for i in range(0,len(block))]
    old_value[0] = block[0]
    for i in range(1,len(block)):
        old_value[i] = block[i]
        block[i] = block[i]^old_value[i-1]

def rowShiftUp(block) :
    temp = block[0]
    for i in range(1,len(block)):
        block[i-1] = block[i]
    block[len(block)-1] = temp

def rowShiftDown(block) :

    # Switch row
    temp = block[len(block)-1]
    for row in range(len(block)-1,0,-1):
        block[row] = block[row-1]
    block[0] = temp

def feistelFunc(block, left_key, right_key):


    for _ in range(len(block)):

        # Cascading XOR
        cascadingXOR(block)
    
        # Row confusion
        rowConfusion(block, right_key)

        # Column confusion
        columnConfusion(block, left_key)

        rowShiftUp(block)

def inverseFeistelFunc(block, left_key, right_key) :

    for _ in range(len(block)):

        rowShiftDown(block)

        # Revert column
        inverseColumnConfusion(block,left_key)


        # Do row addition and wrapping shift
        inverseRowConfusion(block,right_key)

        # Cascading XOR
        inverseCascadingXOR(block)

def main():

    block = bytearray("qwertoui","ascii")
    right_key = bytearray("bCf5g1h/","ascii")
    left_key = bytearray("hg2d7I1_","ascii")

    while (len(block)!=8) or (len(right_key)!=8) or (len(left_key)!=8) :
        print("Input all must be 8 characters")
        block = input("Input block : ")
        right_key = input("Input right key : ")
        left_key = input("Input left key : ")

    feistelFunc(block, left_key, right_key)
    print(block)
    print("==========================")
    inverseFeistelFunc(block, left_key, right_key)
    print(block)

main()