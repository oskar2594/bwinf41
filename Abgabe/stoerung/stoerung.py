# Buch einlesen
with open("beispiele/Alice_im_Wunderland.txt", encoding="utf-8") as file:
    buch = list(filter(None, file.readlines()))

# Gestörte Nachricht einlesen
with open(input("Pfad: "), encoding="utf-8") as file:
    stoerung = file.readline().split(" ")

line_number = 0
list_of_results = []
arr = []

while line_number < len(buch):
    arr += buch[line_number].split(" ")
    while len(arr) > len(stoerung):
        for i, word in enumerate(stoerung):
            if not (word in arr[i] or word.capitalize() in arr[i] or word == "_"):
                # Wenn die Lösung nicht gefunden wird (was die meiste Zeit passiert) wird das erste Wort gelöscht
                arr.pop(0)
                break
            if i == len(stoerung) - 1:
                # hier ist die lösung gefunden worden
                list_of_results.append((" ".join(arr[: len(stoerung)]), line_number))

                # Die gefundene Lösung wird aus arr entfernt
                for g in range(len(stoerung)):
                    arr.pop(0)
                break
    line_number += 1

#Lösungsausgabe
for line, line_number in list_of_results:
    print("line: " + str(line_number + 1))
    print(line)
    print("")
if not list_of_results:
    print("nichts gefunden")
