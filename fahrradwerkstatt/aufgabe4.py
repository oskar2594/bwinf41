import copy


def main():
    with open("beispiel4.txt", "r") as f:
        file = f.read()

    # Auftragszeit und Eingangszeit in zwei Listen,
    # sodass der n-te Auftrag durch die jeweils n-1-ten Elemente dargestellt wird
    start = [int(s) for s in file.split()[::2]]
    work = [int(s) for s in file.split()[1::2]]

    # Anzahl der Auftraege, und die Zeit
    iterations = len(start)
    time = 0

    # Durchlauf der Verfahren mit haesslicher Ausgabe, leicht schoenere in waitresults
    print(first_come_first_serve(start, work, iterations, time))
    print(shortest_job_next(start, work, iterations, time))
    print(highest_response_ratio_next(start, work, iterations, time))


def simulation(i, time_of_order, order_duration, wait, time):
    # time = max(time, time_of_order[i])

    # Wenn die Bearbeitungsdauer den aktuellen Arbeitstag ueberschreitet, wird dieser Arbeitstag beendet
    restarbeitstag = 1020 - time % 1440
    if order_duration[i] > restarbeitstag:
        order_duration[i] -= restarbeitstag
        time += 960 + restarbeitstag

    # Fertigstellungszeit des Auftrages ergibt sich aus der restlichen Arbeitszeit und der Zeit,
    # die zwischen den Arbeitstagen liegt
    time += order_duration[i] + (order_duration[i] // 480) * 960

    # Wartezeiten der verschiedenen Auftraege werden hier gespeichert
    wait.append(time - time_of_order[i])

    return time


def wait_results(wait):  # nur f�r sch�nere Ausgabe gedactht
    max_wait = max(wait)
    averagewait = sum(wait) / len(wait)

    # with open("wartezeiten.txt", "a") as f:
    #     f.write(f"{max_wait:6} || {averagewait:6} \n")
    # print(wait)
    # print('averagewait = ', averagewait, '\nmaxwait = ', max_wait , '\n----------------------------------')


def first_come_first_serve(start, work, iterations, time):
    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)
    for n in range(iterations):
        time = max(time, time_of_order[n])
        time = simulation(n, time_of_order, order_duration, wait, time)
    wait_results(wait)

    return max(wait), sum(wait) / len(wait)


def shortest_job_next(start, work, iterations, time):
    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)
    for j in range(iterations):
        time = max(time, time_of_order[0])

        x = 0
        for i in range(len(time_of_order)):
            if time_of_order[i] > time:
                x = i
                break
        else:
            x = len(time_of_order)

        n = 0
        for i in range(x):
            if order_duration[i] < order_duration[n]:
                n = i
        time = simulation(n, time_of_order, order_duration, wait, time)

        time_of_order.pop(n)
        order_duration.pop(n)
    wait_results(wait)

    return max(wait), sum(wait) / len(wait)


def highest_response_ratio_next(start, work, iterations, time):
    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)
    for j in range(iterations):
        time = max(time, time_of_order[0])
        x = 0
        for i in range(len(time_of_order)):
            if time_of_order[i] > time:
                x = i
                break
        else:
            x = len(time_of_order)

        n = 0
        for i in range(x):
            if (
                1 + (time - time_of_order[i]) / order_duration[i]
                > 1 + (time - time_of_order[n]) / order_duration[n]
            ):
                n = i
        time = simulation(n, time_of_order, order_duration, wait, time)

        time_of_order.pop(n)
        order_duration.pop(n)
    wait_results(wait)

    return max(wait), sum(wait) / len(wait)


if __name__ == "__main__":
    main()
