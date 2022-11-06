with open("Alice_im_Wunderland.txt", 'r') as read_obj:
    with open("stoerung3.txt", "r") as x:
        line_number = 0
        list_of_results = []

        buch = list(filter(None, read_obj.readlines()))

        stoerung = x.readline().split(" ")
        arr = []

        while line_number < len(buch):
            arr += buch[line_number].split(" ")
            while len(arr) > len(stoerung):
                for i, word in enumerate(stoerung):
                    if word in arr[i] or word.capitalize() in arr[i] or word == "_":
                        pass
                    else:
                        arr.pop(0)
                        break
                    if i == len(stoerung) - 1:
                        # hier ist die lösung gefunden worden
                        # man müsste die lösung noch ein bisschen putzen und von allen sonderzeichen befreien, sonst top
                        list_of_results.append((arr[:len(stoerung)], line_number))

                        # auch mit: arr = arr[len(stoerung):]
                        for g in range(len(stoerung)):
                            arr.pop(0)
                            
                        break

            line_number += 1

for x, y in list_of_results:
    print("line: " + str(y))
    print(x)
    print("")
