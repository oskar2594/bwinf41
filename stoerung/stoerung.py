
with open("Alice_im_Wunderland.txt", 'r') as read_obj:
    with open("stoerung0.txt", "r") as x:
        line_number = 0
        list_of_results = []

        buch = list(filter(None, read_obj.readlines()))

        schnipsel = x.readline().split(" ")
        arr = []
        loesung = []
        print(len(schnipsel))
        while line_number < len(buch):
            arr += buch[line_number].split(" ")
            while len(arr) > len(schnipsel):
                for i, word in enumerate(schnipsel):
                    if i + 1 == len(schnipsel):
                        loesung.append(line_number)
                        print(arr)
                        for g in range(len(schnipsel)):
                            arr.pop(0)
                        break
                    if word in arr[i] or word == "_":
                        pass
                    else:
                        arr.pop(0)
                        break

            line_number += 1

for i in loesung:
    print(buch[i])











