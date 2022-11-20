import re
# Buch einlesen
with open("Alice_im_Wunderland.txt", encoding="utf-8") as file:
    buch = list(filter(None, file.readlines()))

# Gestörte Nachricht einlesen
with open(input("Pfad: "), encoding="utf-8") as file:
    stoerung = file.readline()

def get_line_number_of_match(match):
    for line_number, line in enumerate(buch):
        if match in line:
            return line_number
    return -1

list_of_results = []

for match in re.finditer(re.compile(stoerung.replace("_", "(?:[^\s]+)").replace(" ", "(?:\\n|\s)"), re.IGNORECASE | re.MULTILINE), " ".join(buch)):
    list_of_results.append((match.group(0), get_line_number_of_match(match.group(0))))

# Lösungsausgabe
for line, line_number in list_of_results:
    print(f"Match in line {line_number}: {line}")
if not list_of_results:
    print("nichts gefunden")