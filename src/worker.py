import socket
import json
import utils

def run_worker(worker_id, host, port, verbose=False):
	s = socket.socket()
	s.connect((host, port))

	if verbose:
		print(f"[worker] {worker_id} połączony")

	while True:
		msg = f"{worker_id}|GET_TASK\n"
		s.send(msg.encode())

		task = s.recv(4096).decode().strip()

		if task == "NO_TASK":
			if verbose:
				print("[worker] brak zadań, rozłączam")
			break

		if verbose:
			print(f"[worker] {worker_id} robi: {task}")

		result = utils.process_file(task)

		payload = f"{worker_id}|RESULT|{json.dumps(result)}\n"
		s.send(payload.encode())

		ack = s.recv(1024).decode().strip()

	s.close()
