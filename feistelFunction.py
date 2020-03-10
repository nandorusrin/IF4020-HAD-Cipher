class FeistelFunction :

    def __init__(self) :

        pass

    def __rowConfusion(self,block, right_key) :

        for i in range(0,len(block)) :
            block[i] = (block[i] + right_key[i])%256
            
            stride = right_key[i]%8
            mask = 0xFF >> (8-stride)
            temp = (block[i]&mask) << (8-stride)
            block[i] = (block[i] >> stride) + temp

    def __columnConfusion(self,block, left_key) :

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

    def __cascadingXOR(self,block) :
        for row in range(1,len(block)) :
            block[row] = block[row-1]^block[row]

    def __rowShiftUp(self,block) :
        temp = block[0]
        for i in range(1,len(block)):
            block[i-1] = block[i]
        block[len(block)-1] = temp

    def feistelFunc(self, input_block, left_key, right_key):

        block = bytearray(input_block)

        for _ in range(len(block)):

            self.__cascadingXOR(block)
            self.__rowConfusion(block, right_key)
            self.__columnConfusion(block, left_key)
            self.__rowShiftUp(block)

        return block


