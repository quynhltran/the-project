
import math, os

def list_to_string(lst1):
    string = ''.join(lst1)
    return string

def text_to_index(line):
    ''' Converts the given text to bitmap index based on the given files and returns strings'''
    animals = { "cat": "1000", "dog": "0100", "turtle": "0010", "bird": "0001"}
    ages = {
        1: "1000000000",
        2: "0100000000",
        3: "0010000000",
        4: "0001000000",
        5: "0000100000",
        6: "0000010000",
        7: "0000001000",
        8: "0000000100",
        9: "0000000010",
        10: "0000000001" }
    adopted = { "True": "10", "False": "01"}

    new_line = line.strip().rsplit(',')
    string = ''

    # grab the corresponding animals, ages, and adopted boolean

    string += str(animals.get(new_line[0]))
    string += str(ages.get(math.ceil(int(new_line[1])/10)))
    string += str(adopted.get(new_line[2])+ '\n')
    return string

def create_index(input_file, output_path, sorted): 
    fd_input = open(input_file, 'r')

   # list of each line
    data = fd_input.readlines()
    # if sorted is true, create index and sort the data. If not sorted, then proceed
    if sorted:
        data.sort()  # sort the data
        output_file = os.path.join(output_path, input_file + "_sorted")
        
    else:
        output_file = os.path.join(output_path, input_file)
        
    fd_output = open(output_file, 'w')

    for line in data:
        fd_output.write(text_to_index(line)) # write to the new bitmap file
    fd_output.close()

def is_run(chunk): 
    ''' Checks if the chunk is a run or not by comparing each bit with the header'''
   
    for i in range(1, len(chunk)):
        if chunk[0] != chunk[i]:
            return False
    return True

def add_run(chunk,size): 
    ''' creates a chunk with 1s or 0s with the given size'''
    compress = ["1"] 
    compress += str(chunk[0])  
    compress += (["0"] * (size - 2)) + ["1"]
    return compress

def add_literal(chunk, size):
    ''' creates a literal starts with 0 and append the whole chunk'''
    compress = ["0"]
    for i in chunk:
        compress +=i  
    return compress

def add_binary(list1, list2):  # get two lists and add their value as binary, return the sum as a list
    length = len(list1)
    bin1_str = list_to_string(list1)
    bin2_str = list_to_string(list2)

    increment = bin(int(bin1_str, 2) + int(bin2_str, 2)) # binarize the increment 
    increment = list(increment[2:]) # remove the letters in the binary results

    # check if the chunk needs to be padded with 0s
    if len(increment) < length:
        dif = length - len(increment)
        new_incre = ["0"] * dif + increment
        return new_incre

    return increment

def is_run_full(chunk):
    for i in chunk:
        if i == '0':
            return False
    return True

def compress_index(bitmap_index, output_path, compression_method, word_size):
    ''' reads the given file, compresses, and writes the compressed version to a new file with the specified output path'''

    file_name = bitmap_index + '_' + compression_method + '_' + str(word_size)
    output_file = os.path.join(output_path, file_name)

    f_input = open(bitmap_index,'r')
    f_output = open(output_file, 'w')

    data = f_input.readlines()

    if compression_method == 'WAH':
        runs=0
        lits=0
        size=word_size-1
        for col in range(16):
            string = ''
            lst = []

            # store data as string
            for line in data:
                string += line[col]
            # store all the chunks in to lst
            for i in range(0, len(string), size):
                lst += [string[i:(i+size)]]

            compressed = []
            flag = False # if the previous chunk is a run or not

            # iterate through each chunk
            for chunk in lst:

                # if the last chunk does not have enough bits, copy it and pad with 0s
                if len(chunk) < size:  
                    compressed += add_literal(chunk,size)
                    compressed += ["0"] * (size - len(chunk))  
                    break

                # if the chunk is a run
                if is_run(chunk): 
                    runs += 1
                    if len(compressed) == 0:  # first run
                        compressed += add_run(chunk,size)
                        flag = True
                    else:
                        if flag:
                            if compressed[-size] == chunk[0]:  # same run of 1s or Os with the previous chunk
                                previous = compressed[-(size - 1):]

                                # if the run is overflow- start a new run chunk to store
                                if is_run_full(previous):
                                    compressed += add_run(chunk,size)
                                else:
                                    new_val = ["0"] * (size - 2) + ["1"]
                                    compressed = compressed[:(len(compressed) - size + 1)]
                                    # add the binary result
                                    compressed += add_binary(previous, new_val)
                            # if the previous run is different, start a new run chunk
                            else: 
                                compressed += add_run(chunk,size)

                        else:  # previous is a literal
                            compressed += add_run(chunk,size)
                            flag = True
                # if the chunk is a lit
                else:  
                    lits += 1
                    compressed += add_literal(chunk,size)
                    flag = False
            
            # write the compressed version to the file
            f_output.write(list_to_string(compressed) +'\n')
        print('Total run: ',runs)
        print('Total literal: ', lits)
    f_output.close()
    f_input.close()




        
    
   
        



























