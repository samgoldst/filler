import sys
import socket
import random
import select
import getopt

from board import Board

i = 0

_, args = getopt.getopt(sys.argv, "s")

option = input("Server or Client (S/C): ").strip()

if option.upper() == 'S':
    colors = int(input("Number of colors: ").strip())
    Board.set_options(colors)
    rows = int(input("Number of rows: ").strip())
    cols = int(input("Number of columns: ").strip())
    seed = int(input("Seed (0 for random): "))
    port = int(input("Port (0 for default): "))
    if seed == 0:
        seed = random.randint(0, 1 << 32)
        if "-s" in args:
            print("Seed: " + str(seed))
    b = Board((rows, cols), seed)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if port == 0:
        port = 60006
        print("assigned port 60006")
    s.bind(("", port))
    s.listen(5)
    print("Waiting for client to connect...")
    connection, address = s.accept()
    print("Connection complete!")
    connection.sendall(f"{colors},{rows},{cols},{seed}".encode("ascii"))
    print(b.__str__(print_outline=True))
    while True:
        move = input("Your move: ")[0]
        b.play_move(" ", move)
        connection.sendall(move.encode("ascii"))
        print(b.__str__(print_outline=True))
        read_list = []
        print("Waiting for opponent's move...")
        while not read_list:
            read_list, _, _ = select.select([connection], [], [], 10)
        move = connection.recv(100).decode("ascii")
        print("Your opponent played: " + move)
        b.play_move("█", move)
        print(b.__str__(print_outline=True))

elif option.upper() == 'C':
    ip = input("IP of server (\"local\" for local host): ")
    port = int(input("Port (0 for default): "))
    if ip == "local":
        ip = "127.0.0.1"
    if port == 0:
        port = 60006
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Trying to connect to server...")
    s.connect((ip, port))
    print("Connection complete!")
    colors, rows, cols, seed = [int(n) for n in s.recv(100).decode("ascii").split(',')]
    if "-s" in args:
        print("Seed: " + str(seed))
    Board.set_options(colors)
    b = Board((rows, cols), seed)
    print(b.__str__(print_outline=True))
    while True:
        read_list = []
        print("Waiting for opponent's move...")
        while not read_list:
            read_list, _, _ = select.select([s], [], [], 10)
        move = s.recv(100).decode("ascii")
        print("Your opponent played: " + move)
        b.play_move(" ", move)
        print(b.__str__(print_outline=True))
        move = input("Your move: ")[0]
        b.play_move("█", move)
        s.sendall(move.encode("ascii"))
        print(b.__str__(print_outline=True))



# while True:
#     if i & 1:
#         print(Board.minimax(b, False, 5, float("-inf"), float("inf"))[1])
#     move = input()
#     b.play_move("█" if i & 1 else " ", move)
#     i += 1
