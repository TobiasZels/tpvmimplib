from tpvmimplib import TPVM_Connection
import threading

FIFO_PATH = "../"

connection = TPVM_Connection("localhost:3002", False)
copy_paste = connection.add_operation("Fenstername", "copy und paste", lambda: print("works"))

try:
    fifo = open(FIFO_PATH, "w")
    fifo.write(connection.id)
    fifo.close()
    print("success")
except FileNotFoundError:
    print("FIFO not found")

socket_thread = threading.Thread(target=connection.start_connection)
socket_thread.daemon = True
socket_thread.start()


while True:
    # Program loop
    pass

connection.stop_connection()
connection.remove_operation(copy_paste)
connection.delist()