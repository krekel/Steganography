_magic_number = 'P3'


def char_to_bin(string):
    bin_string = [bin(ord(char))[2:].zfill(8) for char in string]
    # Qty of bits for removal purposes pos:1
    bin_string.insert(0, bin((len(bin_string)) * 8)[2:].zfill(8))

    # length of bits length number
    fill = len(bin_string[0])
    length = len(bin_string[0][2:].zfill(fill))
    bin_string.insert(0, bin(length)[2:].zfill(8))
    return bin_string


# Only works for the image being inserted
def ascii_to_bin(data):
    bin_data = []
    width = bin(int(data[0]))[2:].zfill(16)
    height = bin(int(data[1]))[2:].zfill(16)

    for elem in range(2, len(data)):
        bin_data.append(bin(int(data[elem]))[2:].zfill(8))

    # Number of bits to be inserted for removal purposes
    bin_data.insert(0, bin((len(bin_data) * 8))[2:].zfill(22))
    print((len(bin_data) * 8))

    # Insert dimensions
    bin_data.insert(0, height)
    bin_data.insert(0, width)

    return bin_data


def hide_message(message, image):
    bin_msg = char_to_bin(message)

    # Number of bits to be inserted
    bits = int(bin_msg[1], 2)

    try:
        with open(image, 'r') as f:
            header = f.readlines()[0:3]
            f.seek(0)
            data = [y for x in f.readlines()[3:] for y in x.replace("\n", "").split(" ") if y != ""]
    except FileNotFoundError as e:
        print(e.strerror)
    else:

        bin_data = [bin(int(x))[2:].zfill(8) for x in data]

        if len(bin_data) < bits:
            raise ValueError()

        # Inserting Message with LSB technique
        y = 0
        for x in "".join(bin_msg):
            while y < (len(bin_data)):
                bin_data[y] = bin_data[y][0:len(bin_data[y])-1] + x
                y += 1
                break

        # binary to ascii
        for x in range(len(bin_data)):
            data[x] = str(int(bin_data[x], 2)) + "\n"

        with open("stego_" + image, 'w') as f:
            f.write(''.join(header) + ''.join(data))


def retrieve_message(image):

    try:
        with open(image, 'r') as f:
            header = f.readlines()[0:3]
            f.seek(0)
            data = [y for x in f.readlines()[3:] for y in x.replace("\n", "").split(" ") if y != ""]
    except FileNotFoundError as e:
        print(e.strerror)
    else:

        # ascii to binary
        bin_data = [bin(int(x))[2:].zfill(8) for x in data]

        # Retrieve length of ??Qty of bits??
        bit_length = ""
        for x in range(8):
            bit_length += bin_data[x][-1]

        message_length = ""
        # Retrieve Message Length (Bits Qty)
        for x in range(8, 8 + int(bit_length, 2)):
            message_length += bin_data[x][-1]

        bin_msg = []
        # Retrieve Message
        ctr = 0
        acc = ""
        x = 8 + int(bit_length, 2)
        y = x + int(message_length, 2)

        while x < y:
            if ctr < 8:
                acc += bin_data[x][-1]
                ctr += 1
                x += 1
            else:
                bin_msg.append(acc)
                acc = ""
                ctr = 0
        bin_msg.append(acc)

        message = ""
        for x in bin_msg:
            message += chr(int(x, 2))

        return message


def hide_image(secret, carrier):

    try:
        with open(secret, "r") as a, open(carrier, "r") as b:

            secret_data = [y for x in a.readlines()[1:] for y in x.replace("\n", "").split(" ") if y != ""]

            carrier_header = b.readlines()[0:3]
            b.seek(0)
            carrier_data = [y for x in b.readlines()[3:] for y in x.replace("\n", "").split(" ") if y != ""]

    except FileNotFoundError:
        print(FileNotFoundError.strerror)
    else:

        bin_carrier_data = [bin(int(x))[2:].zfill(8) for x in carrier_data]
        bin_secret_data = "".join(ascii_to_bin(secret_data))

        if len(bin_secret_data) > len(bin_carrier_data):
            raise ValueError()

        # Insert image into carrier
        y = 0
        bit_pos = 1
        for x in bin_secret_data:
            if y < len(bin_carrier_data):
                if bit_pos > 1:
                    bin_carrier_data[y] = bin_carrier_data[y][0:len(bin_carrier_data[y]) - bit_pos] + \
                                          x + \
                                          bin_carrier_data[y][-bit_pos + 1:]
                    y += 1
                else:
                    bin_carrier_data[y] = bin_carrier_data[y][0:len(bin_carrier_data[y]) - bit_pos] + x
                    y += 1
            else:
                y = 0
                bit_pos += 1
                bin_carrier_data[y] = bin_carrier_data[y][0:len(bin_carrier_data[y]) - bit_pos] + x + bin_carrier_data[y][-bit_pos + 1:]
                y += 1

        for x in range(len(bin_carrier_data)):
            carrier_data[x] = str(int(bin_carrier_data[x], 2))

        with open('steg_' + carrier, 'w') as f:
            f.write("".join(carrier_header) + "\n".join(carrier_data))


def retrieve_image(image):

    try:
        with open(image, 'r') as f:

            header_bin = [bin(int(y))[2:].zfill(16) for x in f.readlines()[3:35] for y in x.replace("\n", "").split(" ") if y != ""]
            f.seek(0)
            l = [bin(int(y))[2:].zfill(16) for x in f.readlines()[35:57] for y in x.replace("\n", "").split(" ") if y != ""]
            f.seek(0)
            data_bin = [bin(int(y))[2:].zfill(16) for x in f.readlines()[57:] for y in x.replace("\n", "").split(" ") if y != ""]

    except FileNotFoundError:
        print(FileNotFoundError.strerror)
    else:

        # Extract header
        h = ''
        for x in range(32):
            h += header_bin[x][-1]

        header = _magic_number + "\n" + str(int(h[0:16], 2)) + " " + str(int(h[16:33], 2)) + "\n"

        #Extract data
        message_length = ''
        for x in range(len(l)):
            message_length += l[x][-1]

        message_length = int(message_length, 2)

        d = ''
        y = 0
        bit_pos = -1
        for x in range(message_length):
            if y < len(data_bin):
                d += data_bin[y][bit_pos]
                y += 1
            else:
                y = 0
                bit_pos -= 1
                d += data_bin[y][bit_pos]
                y += 1

        data = []
        acc = ''
        y = 0
        for x in d:
            if y < 8:
                acc += x
                y += 1
            else:
                data.append(str(int(acc, 2)))
                y = 0
                acc = ''
                acc += x
                y += 1

        data.append(str(int(acc, 2)))
        data.append("")

        with open("ret_image.ppm", 'w') as f:
            f.write("".join(header) + "\n".join(data))
