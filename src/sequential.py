import string
from pathlib import Path
import utils

def count_words(words):
	counts = {}

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1

	return counts


def process_text(filepath):
	with open(filepath, "r", encoding="utf-8") as f:
		text = f.read()

		# Małe litery
		text = text.lower()

		# Usuniecie interpunkcji
		text = text.translate(str.maketrans("", "", string.punctuation))

		# Tokenizacja
		words = text.split()

		# Zliczanie słów
		counts = count_words(words)

		return counts


def coordinate():
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

	for plik in files:
		try:
			counts = process_text(plik)
			print(counts)

		except Exception as e:
			print("błąd pliku: ", e)


# Uruchom
coordinate()