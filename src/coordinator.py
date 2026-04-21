import socket
import threading
import time
import utils
import multiprocessing as mp
from pathlib import Path
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


def run_coordinator(workers=2, data_dir=None, verbose=False):
	total_start = time.perf_counter()

	# Ścieżki
	base_dir = Path(__file__).parent.parent  # wyjscie z src
	if data_dir is None:
		data_path = base_dir / "dane"
	else:
		data_path = (base_dir / data_dir).resolve()

	# Wczytywanie plików
	files = list(data_path.glob("*.txt"))

	if not files:
		print("[coordinator] błąd pliku: brak plików w folderze")
		return

	# Rodzielanie pracy
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
		if verbose:
			print("[coordinator] worker połączony:", _addr)

		while True:
			msg = _conn.recv(4096).decode().strip()

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
			elif message.startswith("RESULT|"):
				import json
				result = json.loads(message.split("|", 1)[1])
				_collector.add_result(_worker_id, result)
				_conn.send("OK\n".encode())

		_conn.close()

	# tcp server
	host = "127.0.0.1"
	port = 5000

	s = socket.socket()
	s.bind((host, port))
	s.listen(workers)

	if verbose:
		print("[coordinator] serwer uruchomiony na: ", host, port)

	# start workerów
	processes = start_workers(workers, host, port)

	for i in range(workers):
		conn, addr = s.accept()
		threading.Thread(
			target=handle_worker,
			args=(conn, addr, collector),
			daemon=True
		).start()

	map_start = time.perf_counter()

	collector.complete_event.wait()

	map_end = time.perf_counter()

	# zamknij procesy workerów
	for p in processes:
		p.join()

	reduce_start = time.perf_counter()
	# REDUCE
	word_count = utils.merge_results(collector.results)
	word_count = utils.top_k_words(word_count)
	#
	reduce_end = time.perf_counter()

	total_end = time.perf_counter()

	# METRYKI
	map_time = map_end - map_start
	reduce_time = reduce_end - reduce_start
	total_time = total_end - total_start

	# WYNIKI
	if verbose:
		print("TOP 20:", word_count)
		print(f"MAP time:     {map_time:.6f}s")
		print(f"REDUCE time:  {reduce_time:.6f}s")
		print(f"TOTAL time:   {total_time:.6f}s")

	return word_count, total_time, map_time, reduce_time


if __name__ == "__main__":
	# run_coordinator()
	pass
