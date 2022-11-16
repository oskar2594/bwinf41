# Buch einlesen
with open("Alice_im_Wunderland.txt", encoding="utf-8") as file:
    buch = list(filter(None, file.readlines()))

# Gestörte Nachricht einlesen
with open(input("Pfad: ")) as file:
    stoerung = file.readline().split(" ")

line_number = 0
list_of_results = []
arr = []

while line_number < len(buch):
    arr += buch[line_number].split(" ")
    while len(arr) > len(stoerung):
        for i, word in enumerate(stoerung):
            if not (word in arr[i] or word.capitalize() in arr[i] or word == "_"):
                arr.pop(0)
                break
            if i == len(stoerung) - 1:
                # hier ist die lösung gefunden worden
                # man müsste die lösung noch ein bisschen putzen 
                # und von allen sonderzeichen befreien, sonst top
                list_of_results.append((" ".join(arr[: len(stoerung)]), line_number))

                # auch mit: arr = arr[len(stoerung):]
                for g in range(len(stoerung)):
                    arr.pop(0)
                break
    line_number += 1

for line, line_number in list_of_results:
    print("line: " + str(line_number))
    print(line)
    print("")
