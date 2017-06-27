

def hide_message(message, image):

    ascii_values = [str(len(message))]
    for x in message:
        ascii_values.append(str(ord(x)).zfill(3))

    try:
        with open(image, "r") as f:
            data = f.readlines()

        # for line in data:
        #     print(line.replace(b"\n", b""))
        #
        # for x in ascii_values:
        #
        #
        # for x in range(3, len(data)):
        #     for y in range(len(data[x])):
        #         data[x][y] = [len(data[x][y]) - 1:] +

        print(data)


    except FileNotFoundError as e:
        print(e.strerror)




hide_message("hello", "castillo.ppm")