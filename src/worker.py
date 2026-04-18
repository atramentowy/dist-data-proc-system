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

	print("worker połączony: " + str(worker_id))
	result = "test1234"

	payload = f"{worker_id}|{result}"
	s.send(payload.encode())

	print("worker: wysłano wynik")

	s.close()

# import socket
# import time
#
#
# def worker(worker_id, queue):
# 	s = socket.socket()
# 	s.connect(("127.0.0.1", 5000))
#
#     time.sleep(1 + worker_id) # symulacja pracy
#     result = f"wynik {worker_id}"
#
#     queue.put((worker_id, result))
# 	s.close()


# map phase
# receive text
# split words
# count words
# send dict back
