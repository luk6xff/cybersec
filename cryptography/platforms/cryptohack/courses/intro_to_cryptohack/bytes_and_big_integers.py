# https://cryptohack.org/courses/intro/enc4/

DATA = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

# Convert the number to hex and then to bytes
hex_data = hex(DATA)[2:]
print(f'Hex data: {hex_data}')
binary_data = bytes.fromhex(hex_data)
print(f'Binary data: {binary_data}')
string_data = binary_data.decode('ascii')
print(f'String data: {string_data}')
