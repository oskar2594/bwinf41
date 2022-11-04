
with open("Alice_im_Wunderland.txt", 'r') as read_obj:
    with open("stoerung0.txt", "r") as x:
        line_number = 0
        list_of_results = []

        buch = list(filter(None, read_obj.readlines()))

        schnipsel = x.readline().split(" ")
        arr = []
        loesung = []

        while line_number < len(buch):
            arr += buch[line_number].split(" ")
            while len(arr) > len(schnipsel):
                for i, word in enumerate(schnipsel):
                    if word in arr[i]:
                        if word == "_":
                            pass
                    else:
                        arr.pop(0)
                        break
                    print(buch[line_number-1] + buch[line_number])
            line_number += 1













