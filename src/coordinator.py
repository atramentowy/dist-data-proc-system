import socket
import threading
import multiprocessing as mp
from pathlib import Path

import utils
from worker import run_worker

class ResultCollector:
	def __init__(self, expected_workers):
		self.results = {}
		self.expected_workers = expected_workers
		self.lock = threading.Lock()
		self.complete_event = threading.Event()

	def add_result(self, worker_id, result):
		with self.lock:
			self.results[worker_id] = result
			if len(self.results) == self.expected_workers:
				self.complete_event.set()


# def worker(worker_id, queue):
#     time.sleep(1 + worker_id)  # symulacja pracy
#     result = f"wynik {worker_id}"
#     queue.put((worker_id, result))

def start_workers(num_workers, coord_host, coord_port):
	processes = []

	for worker_id in range(num_workers):
		p = mp.Process(
			target=run_worker,
			args=(worker_id, coord_host, coord_port)
		)

		p.start()
		processes.append(p)

	return processes


def run_coordinator():
	# Generowanie plików testowych
	utils.generate_test_file("data1", 1000)
	utils.generate_test_file("data2", 1000)

	# Ścieżki
	base_dir = Path(__file__).parent.parent  # wyjscie z src
	data_dir = base_dir / "dane"

	# Wczytywanie plików
	files = list(data_dir.glob("*.txt"))

	if not files:
		print("błąd pliku: brak plików w folderze")
		return

	# Rodzielanie pracy
	# metoda: round-robin
	workers = 2

	assignments = [[] for _ in range(workers)]

	for i, file in enumerate(files):
		assignments[i % workers].append(file)

	# result collector
	collector = ResultCollector(workers)

	# tcp server
	coord_host = "127.0.0.1"
	coord_port = 5000

	s = socket.socket()
	s.bind((coord_host, coord_port))
	s.listen(workers)

	print("serwer uruchomiony na: ", coord_host, coord_port)

	# start workerów
	processes = start_workers(workers, coord_host, coord_port)

	try:
		for _ in range(workers):
			conn, addr = s.accept()

			conn.settimeout(5)
			data = conn.recv(4096).decode()

			if "|" not in data:
				print("BŁĘDNE DANE:", data)
				continue

			try:
				worker_id_str, result_str = data.split("|", 1)
			except ValueError:
				print("uszkodzone dane:", data)
				continue

			worker_id = int(worker_id_str)

			collector.add_result(worker_id, result_str)

	finally:
		s.close()

	print("wyniki: ", collector.results)

	# zakończ procesy workerów
	for p in processes:
		p.join()


if __name__ == "__main__":
	run_coordinator()
