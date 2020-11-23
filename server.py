import socket
import datetime
import sqlite3

SERVER_ADDRESS = '127.0.0.1', 54322

with sqlite3.connect('data.sqlite') as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS station_status (
            station_id INTEGER PRIMARY KEY NOT NULL,
            last_date TEXT,
            alarm1 INTEGER,
            alarm2 INTEGER
            );
    """)

with socket.socket() as accept_socket:
    accept_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        accept_socket.bind(SERVER_ADDRESS)
    except OSError:
        print("port {} is already in use. Try changing the port number or clearing it.".format(SERVER_ADDRESS[1]))
    else:
        accept_socket.listen(16)
        print("Server is now listening on {}:{}".format(*SERVER_ADDRESS))

        while True:
            client, client_address = accept_socket.accept()
            data = client.recv(1024)
            try:
                station_id, alarm1, alarm2 = data.decode().split(' ')
            except UnicodeError:
                print("{}:{} sent non-UTF8 message. can't read".format(*client_address))
                continue
            else:
                try:
                    station_id, alarm1, alarm2 = int(station_id), int(alarm1), int(alarm2)
                except ValueError:
                    print("Data is not matching file format. Station_id, alarm1 and alarm2 must be integers")
                    continue
                else:
                    last_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    cur = conn.execute("""
                                        INSERT OR REPLACE INTO station_status VALUES
                                        (?, ?, ?, ?)""", (station_id, last_date, alarm1, alarm2))
                    cur.execute("SELECT * FROM station_status")
                    print("Station status update:")
                    for line in cur:  # Print the status of all stations in the database.
                        print("""---------------------
station id: {}\nlast update: {}\nalarm 1: {}\nalarm 2: {}
---------------------""".format(*line))
