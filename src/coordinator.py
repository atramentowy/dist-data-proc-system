import socket
import threading
import multiprocessing as mp
from pathlib import Path

import utils
from worker import run_worker


class ResultCollector:
	def __init__(self, expected_results):
		self.results = []
		self.expected_results = expected_results
		self.lock = threading.Lock()
		self.complete_event = threading.Event()

	def add_result(self, worker_id, result):
		with self.lock:
			# self.results[worker_id] = result
			self.results.append(result)
			if len(self.results) == self.expected_results:
				self.complete_event.set()


def start_workers(num_workers, coord_host, coord_port):
	processes = []

	for w_id in range(num_workers):
		p = mp.Process(
			target=run_worker,
			args=(w_id, coord_host, coord_port)
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
		print("[coordinator] błąd pliku: brak plików w folderze")
		return

	# Rodzielanie pracy
	workers = 2

	# round-robin
	assignments = [files[i::workers] for i in range(workers)]

	collector = ResultCollector(len(files))

	lock = threading.Lock()

	def get_task(_worker_id):
		with lock:
			if assignments[_worker_id]:
				return assignments[_worker_id].pop()
			return None

	def handle_worker(_conn, _addr, _collector):
		print("[coordinator] worker connected:", _addr)

		while True:
			msg = _conn.recv(1024).decode().strip()

			if "|" not in msg:
				continue

			_worker_id, message = msg.split("|", 1)
			_worker_id = int(_worker_id)

			# worker prosi o task
			if message == "GET_TASK":
				_task = get_task(_worker_id)

				if _task is not None:
					_conn.send(str(_task).encode())
				else:
					_conn.send(str("NO_TASK").encode())
					break

			# worker wysyła wynik
			else:
				_collector.add_result(_worker_id, message)
				_conn.send("OK\n".encode())

		_conn.close()

	# tcp server
	coord_host = "127.0.0.1"
	coord_port = 5000

	s = socket.socket()
	s.bind((coord_host, coord_port))
	s.listen(workers)

	print("[coordinator] serwer uruchomiony na: ", coord_host, coord_port)

	# start workerów
	processes = start_workers(workers, coord_host, coord_port)

	for i in range(workers):
		conn, addr = s.accept()
		threading.Thread(
			target=handle_worker,
			args=(conn, addr, collector),
			daemon=True
		).start()

	collector.complete_event.wait()
	print(collector.results)

	for p in processes:
		p.join()


if __name__ == "__main__":
	run_coordinator()
