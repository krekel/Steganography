

# TODO size restrictions - message can't be greater than image
def hide_message(message, image):

    """Hide a string inside a ppm image.

    :param message: string to be inserted into the image
    :param image: ppm image
    :return:
    """

    # Convert message to ascii
    ascii_message = [x for x in str(len(message)).zfill(3)]
    for x in message:
        for y in str(ord(x)).zfill(3):
            ascii_message.append(y)

    try:
        with open(image, "r") as f:
            header = f.readlines()[0:3]
            f.seek(0)
            data = f.readlines()[3:]

    except FileNotFoundError as e:
        print(e.strerror)
    else:
        # Image data (no header information)
        # Store each line of data in a 2d array for better access.
        # Last value of each line is \n
        image_data = [line.split(" ") for line in data]

        # Insert message
        z = 0
        for x in range(len(image_data)):
            for y in range(len(image_data[x])):
                while z < len(ascii_message):
                    if image_data[x][y] != "\n":
                        image_data[x][y] = image_data[x][y][0:len(image_data[x][y]) - 1] + ascii_message[z]
                        z += 1
                    break

        # Add header information to image data
        stego_image = ""
        for elem in header:
            stego_image += elem

        for x in range(len(image_data)):
            for y in range(len(image_data[x])):
                if image_data[x][y] == "\n":
                    stego_image += image_data[x][y]
                else:
                    stego_image += image_data[x][y] + " "

        # Create stego image
        with open("stego_" + image, 'w') as f:
            f.write(stego_image)


def retrieve_message(image):

    try:
        with open(image, "r") as f:
            header = f.readlines()[0:3]
            f.seek(0)
            data = f.readlines()[3:]

    except FileNotFoundError as e:

        print(e.strerror)

    else:

        # Image data (no header information)
        # Store each line of data in a 2d array for better access.
        # Last value of each line is \n
        image_data = [line.split(" ") for line in data]

        # Get message length
        length = ""
        for x in range(3):
            length += image_data[0][x][-1]
        print(length)

        ascii_values = ""
        # Extract message
        z = 0
        for x in range(len(image_data)):
            for y in range(len(image_data[x])):
                while z < (int(length) * 3) + 3:
                    if image_data[x][y] != "\n":
                        ascii_values += image_data[x][y][-1]
                        z += 1
                    break

        # Convert from ascii to chr
        message = ""
        for x in range(3, len(ascii_values), 3):
            message += chr(int(ascii_values[x:x + 3]))

    return message


def hide_image(secret, carrier):

    with open(secret, "r") as a, open(carrier, "r") as b:
        secret_data = []
        for x in a.readlines()[1:]:
            for y in x.split(" "):
                if y != "\n":
                    for z in y.zfill(3):
                        if z != "\n":
                            secret_data.append(z)

        carrier_header = b.readlines()[0:3]
        b.seek(0)
        carrier_data = [y for x in b.readlines()[3:] for y in x.split(" ")]

        print(carrier_header)

    # Insert secret image into carrier image
    x = 0
    for y in range(len(carrier_data)):
        while x < len(secret_data):
            if carrier_data[y] != "\n":
                carrier_data[y] = carrier_data[y][0:2] + secret_data[x]
            x += 1
            break

    with open("stego_" + carrier, "w") as f:
        f.write("".join(carrier_header) + " ".join(carrier_data))








def retrieve_image():
    None

# hide_message("Hola me llamo tito. Esto es un mensaje secreto shhh", "casstillo.ppm")
# m = retrieve_message("stego_castillo.ppm")
# print(m)
hide_image("castillo.ppm", "cotorra_boricua.ppm")
