from pathlib import Path
import random
import time

def generate_test_file(filename, num_words=1000):
	base_dir = Path(__file__).parent.parent  # wyjście z src/
	folder = base_dir / "dane"

	folder.mkdir(exist_ok=True)

	filepath = folder / f"{filename}.txt"  # pełna ścieżka
	if not filepath.is_file():
		print("plik testowy: generuję")

		words = ['python', 'programming', 'distributed', 'system', 'data', 'processing', 'parallel', 'computing']
		with open(filepath, 'w') as f:
			for _ in range(num_words):
				word = random.choice(words)
				f.write(word + ' ')

		print("plik testowy: wygenerowano pomyślnie")


def measure_performance(func, *args):
	start_time = time.time()

	result = func(*args)
	end_time = time.time()
	execution_time = end_time - start_time
	return result, execution_time
