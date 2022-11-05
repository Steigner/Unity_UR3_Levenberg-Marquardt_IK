import zmq
import time
from IK import IK_LM

def send_array(socket, A):
    msg = dict(
        dtype = str(A.dtype),
        shape = A.shape,
        data = A.tolist()
    )
    socket.send_json(msg)

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        print("Server On")
        # wait for receive message
        msg = socket.recv()
        time.sleep(0.5)
        if (msg.decode("utf-8") == "Start Compute"):   
            # compute and send as json dict
            a = IK_LM().LM()
            send_array(socket, a)

if __name__ == "__main__":
    start_server()