import string
import socket

def count_words(words):
	counts = {}

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1

	return counts


def process_file(filepath):  # MAP
	with open(filepath, "r", encoding="utf-8") as f:
		text = f.read()

		# Małe litery
		text = text.lower()

		# Usuniecie interpunkcji
		text = text.translate(str.maketrans("", "", string.punctuation))

		# Tokenizacja
		words = text.split()

		# Usuwanie liczb
		# Usuwa tokeny będące tylko liczbami, pozostawia ciągi alfanumeryczne
		words = [w for w in words if not w.isdigit()]

		# Zliczanie słów
		counts = count_words(words)

		return counts


def run_worker(worker_id, host, port):
	s = socket.socket()
	s.connect((host, port))

	print("[worker] połączony: " + str(worker_id))

	while True:
		msg = f"{worker_id}|GET_TASK\n"
		s.send(msg.encode())

		task = s.recv(1024).decode().strip()

		if task == "NO_TASK":
			print("[worker] brak zadan koncze")
			break

		print(f"[worker] {worker_id} robi: {task}")

		result = process_file(task)

		payload = f"{worker_id}|{result}\n"
		s.send(payload.encode())

		ack = s.recv(1024).decode().strip()

	s.close()
