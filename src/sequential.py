import time
from pathlib import Path
import utils


def run_sequential():
	total_start = time.perf_counter()

	# Generowanie plików testowych
	# utils.generate_test_file("data1", 1000)
	# utils.generate_test_file("data2", 1000)

	# Ścieżki
	base_dir = Path(__file__).parent.parent  # wyjscie z src
	data_dir = base_dir / "dane"

	# Wczytywanie plików
	files = list(data_dir.glob("*.txt"))

	# Podział pracy
	if not files:
		print("[sequential] błąd danych: brak plików w folderze")

	map_start = time.perf_counter()

	results = []
	for file in files:
		# Worker
		result = utils.process_file(file)
		results.append(result)

	map_end = time.perf_counter()

	reduce_start = time.perf_counter()
	# REDUCE
	word_count = utils.merge_results(results)
	word_count = utils.top_k_words(word_count)
	#
	reduce_end = time.perf_counter()

	total_end = time.perf_counter()

	# METRYKI
	map_time = map_end - map_start
	reduce_time = reduce_end - reduce_start
	total_time = total_end - total_start

	# WYNIKI
	print("TOP 20:", word_count)
	print(f"MAP time:     {map_time:.6f}s")
	print(f"REDUCE time:  {reduce_time:.6f}s")
	print(f"TOTAL time:   {total_time:.6f}s")

	return word_count, total_time, map_time, reduce_time


# Uruchom
run_sequential()
