_magic_number = 'P3'


def char_to_bin(string):
    bin_string = [bin(ord(char))[2:].zfill(8) for char in string]
    # Qty of bits for removal purposes pos:1
    bin_string.insert(0, bin((len(bin_string)) * 8)[2:].zfill(8))
    print(bin_string[0])

    # length of bits length number
    fill = len(bin_string[0])
    length = len(bin_string[0][2:].zfill(fill))
    bin_string.insert(0, bin(length)[2:].zfill(8))
    return bin_string


def ascii_to_bin(string):
    bin_string = [bin(int(elem))[2:].zfill(8) for elem in string]
    # Qty of bits for removal purposes
    bin_string.insert(0, bin((len(bin_string)) * 8)[2:].zfill(8))
    print(bin_string[0])

    # length of bits length number
    fill = len(bin_string[0])
    length = len(bin_string[0][2:].zfill(fill))
    bin_string.insert(0, bin(length)[2:].zfill(8))
    return bin_string


def hide_message(message, image):
    bin_msg = char_to_bin(message)
    print(bin_msg)

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

        # ascii to bin
        bin_data = [bin(int(x))[2:].zfill(8) for x in data]

        print(len(bin_data), bits)

        if len(bin_data) < bits:
            raise Exception("Message to big for carrier.")

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

        print(int(bit_length, 2))


        message_length = ""
        # Retrieve Message Length (Bits Qty)
        for x in range(8, 8 + int(bit_length, 2)):
            message_length += bin_data[x][-1]

        print(int(message_length, 2))

        bin_msg = []
        # Retrieve Message
        ctr = 0
        acc = ""
        x = 8 + int(bit_length, 2)
        y = x + int(message_length, 2)
        print(x, y)
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

    with open(secret, "r") as a, open(carrier, "r") as b:
        secret_data = [y for x in a.readlines()[1:] for y in x.replace("\n", "").split(" ") if y != ""]

        carrier_header = b.readlines()[0:3]
        b.seek(0)
        carrier_data = [y for x in b.readlines()[3:] for y in x.replace("\n", "").split(" ") if y != ""]

    bin_secret_data = ascii_to_bin(secret_data)
    bin_carrrier_data = ascii_to_bin(carrier_data)

    if int(bin_secret_data[1], 2) > int(bin_carrrier_data[1], 2):
        raise Exception("Image is to big for carrier")

    # Insert secret image into carrier image
    y = 0
    for x in "".join(bin_secret_data):
        while y < (len(bin_carrrier_data)):
            bin_carrrier_data[y] = bin_carrrier_data[y][0:len(bin_carrrier_data[y]) - 1] + x
            y += 1
            break

    # Convert carrier image back to ascii
    for x in range(len(bin_carrrier_data)):
        carrier_data[x] = str(int(bin_carrrier_data[x], 2)) + "\n"

    with open("stego_" + carrier, "w") as f:
        f.write("".join(carrier_header) + "".join(carrier_data))


def retrieve_image():
    None

# hide_message("Hola me llamo lastier de lasssllklllllllll pls lloiju jugjb juuh"
#              "falkjdlkajeiieiefjfoefeee"
#              "eeefefefwfqefqfqfqfqfq"
#              "qfqefqwefqwefqewfqe $%^ eioqeiuroroo\nkeieieieeiqoeij;adflkqjeflkj"
#              "ad;lfkja;lkdfj;lakjdf;lakjfa"
#              "alkdjl;fkjaldfkjd", "castillo.ppm")
# m = retrieve_message("stego_castillo.ppm")
# print(m)
hide_image("castillo.ppm", "lancia_stratos.ppm")
