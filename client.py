import socket
import time

SERVER_ADDRESS = '127.0.0.1', 54322
SLEEP_TIME = 60


def check_errors(content_list):
    """Checks that the list contains all information as requested in the project description.
    If the file was updated correctly the list should contain 3 items that are convertible
    to integers."""

    if len(content_list) != 3:
        return "Error 1"
    for item in content_list:
        if item == "":
            return "Error 2"
    try:
        content_list = [int(i) for i in content_list]
    except ValueError:
        return "Error 3"
    else:
        return content_list


while True:
    with socket.socket() as client_socket:
        try:  # Check that the file exists
            status_file = open('status.txt', 'r')
        except FileNotFoundError:
            print("File not found. Check that the name of the file is spelled correctly and exists.")
            break
        else:
            file_contents = []
            for line in status_file:
                line = line.strip()
                file_contents.append(line)

            status_file.close()

            file_contents = check_errors(file_contents)
            if file_contents in ('Error 1', 'Error 2', 'Error 3'):
                print("""Incorrect file structure.
Please update status.txt file according to the project description""")
                break

            else:
                data = "{} {} {}".format(*file_contents).encode()  # prepare encoded data as a string
                try:
                    client_socket.connect(SERVER_ADDRESS)
                except ConnectionRefusedError:
                    print("Failed to connect to server. Check that the server is up and running.")
                    break
                else:
                    client_socket.send(data)
                    print("Data sent successfully")
                    client_socket.close()
                    time.sleep(SLEEP_TIME)

print("Goodbye")
