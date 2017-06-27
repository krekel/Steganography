

def hide_message(message, image):

    # Convert message to ascii
    ascii_message = [x for x in str(len(message)).zfill(3)]
    for x in message:
        for y in str(ord(x)).zfill(3):
            ascii_message.append(y)

    print(ascii_message)

    try:
        with open(image, "r") as f:
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

        # print(data[0])
        # print(data[1])
        #
        # print(image_data[0])
        # print(image_data[1])



    except FileNotFoundError as e:
        print(e.strerror)




hide_message("hello", "castillo.ppm")