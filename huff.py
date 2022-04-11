import re
import numpy as np
from PIL import Image, ImageOps

# Function to make the huffman tree
def combine_nodes(nodes):
    pos = 0
    newnode = []
    if len(nodes) > 1:
        nodes.sort()
        nodes[pos].append("1")                     
        nodes[pos+1].append("0")
        combined_node1 = (nodes[pos][0] + nodes[pos+1][0])
        combined_node2 = (nodes[pos][1] + nodes[pos+1][1])
        newnode.append(combined_node1)
        newnode.append(combined_node2)
        newnodes=[]
        newnodes.append(newnode)
        newnodes = newnodes + nodes[2:]
        nodes = newnodes
        huffman_tree.append(nodes)
        combine_nodes(nodes)
    return huffman_tree

img = Image.open('./image.jpg')
img = ImageOps.exif_transpose(img)          
img = img.resize((600, 600))
img.show()
img_matrix = np.asarray(img, np.uint8)
img_shape = img_matrix.shape
img_string = str(img_matrix.tolist())

# Calculating the frequency of characters present in image string
nodes = []
only_letters = []
for letter in img_string:
    if letter not in only_letters:
        frequency = img_string.count(letter)             
        nodes.append([frequency, letter])
        only_letters.append(letter)
                           
nodes.sort()
huffman_tree = []
huffman_tree.append(nodes)

newnodes = combine_nodes(nodes)

huffman_tree.sort(reverse = True)

checklist = []
for level in huffman_tree:
    for node in level:
        if node not in checklist:
            checklist.append(node)
        else:
            level.remove(node)

# Generating the binary code
letter_binary = []
if len(only_letters) == 1:
    lettercode = [only_letters[0], "0"]
    letter_binary.append(lettercode*len(img_string))
else:
    for letter in only_letters:
        code =""
        for node in checklist:
            if len (node)>2 and letter in node[1]:        
                code = code + node[2]
        lettercode =[letter,code]
        letter_binary.append(lettercode)

print("Binary code generated:")
for letter in letter_binary:
    print(letter[0], letter[1])

bitstring = ""
for character in img_string:
    for item in letter_binary:
        if character in item:
            bitstring = bitstring + item[1]
binary = "0b" + bitstring

print("The encoded string is put into file")
output = open("compressed.txt","w+")
print("Compressed file generated as compressed.txt")
output = open("compressed.txt","w+")
output.write(bitstring)

uncompressed_file_size = len(img_string) * 7
compressed_file_size = len(binary) - 2
print("Original file size was ", uncompressed_file_size," bits.")
print("The compressed size is ", compressed_file_size, " bits.")
print("Compression ratio is ", uncompressed_file_size / compressed_file_size)
print("Decoding.......")


# Decoding the image
bitstring = str(binary[2:])
uncompressed_string = ""
code = ""
for digit in bitstring:
    code = code + digit
    pos = 0                                        
    for letter in letter_binary:
        if code == letter[1]:
            uncompressed_string = uncompressed_string + letter_binary[pos][0]
            code = ""
        pos += 1

temp = re.findall(r'\d+', uncompressed_string)
res = list(map(int, temp))
res = np.array(res)
res = res.astype(np.uint8)
res = np.reshape(res, img_shape)
res = Image.fromarray(res)
res.show()