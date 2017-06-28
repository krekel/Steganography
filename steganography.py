

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
                stego_image += image_data[x][y] + " "

        # Create stego image
        with open("stego_"+image, 'w') as f:
            f.write(stego_image)

    except FileNotFoundError as e:
        print(e.strerror)


def get_message(image):

    try:
        with open(image, "r") as f:
            data = f.readlines()[3:]

        # Image data (no header information)
        # Store each line of data in a 2d array for better access.
        # Last value of each line is \n
        image_data = [line.split(" ") for line in data]

        # Get message length
        length = ""
        for x in range(3):
            length += image_data[0][x]



        # Insert message
        z = 0
        for x in range(len(image_data)):
            for y in range(len(image_data[x])):
                while z < len(ascii_message):
                    if image_data[x][y] != "\n":
                        image_data[x][y] = image_data[x][y][0:len(image_data[x][y]) - 1] + ascii_message[z]
                        z += 1
                    break

        # print(data[0])
        # print(data[1])
        #
        # print(image_data[0])
        # print(image_data[1])
        # print(image_data[2])
    except FileNotFoundError as e:
        print(e.strerror)


hide_message("hello my name is", "castillo.ppm")
