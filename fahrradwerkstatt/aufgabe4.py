import copy


def main():
    # Einlese der Eingabedatei
    with open("beispiel0.txt", "r") as f:
        file = f.read()

    # Auftragszeit und Eingangszeit jeweils in Liste
    start = [int(s) for s in file.split()[::2]]
    work = [int(s) for s in file.split()[1::2]]

    # Anzahl der Auftraege, und die Zeit
    iterationen = len(start)
    Zeit = start[0]

    # fuer den Fall, dass Auftrag ausserhalb Arbeitszeit gestellt wurde
    if Zeit % 1440 < 540:
        Zeit += 540 - Zeit % 1440
    elif Zeit % 1440 > 1020:
        Zeit += 1980 - Zeit % 1440

    first_come_first_serve(start, work, iterationen, Zeit)
    shortest_job_next(start, work, iterationen, Zeit)
    highest_response_ratio_next(start, work, iterationen, Zeit)


def simulation(i, time_of_order, order_duration, wait, time):

    i_duration = order_duration[i]
    work_day_left = 1020 - time % 1440
    if i_duration > work_day_left:
        time += i_duration + (1 + ((i_duration - work_day_left) // 480)) * 960
    else:
        time += i_duration

    wait.append(time - time_of_order[i])
    time_of_order.pop(i)
    order_duration.pop(i)

    # Startzeit des naechsten Auftrages
    if len(order_duration) > 0:
        time = max(time, time_of_order[0])
        if time % 1440 < 540:
            time += 540 - time % 1440
        elif time % 1440 > 1020:
            time += 1980 - time % 1440

    return time


def wait_results(wait, name):

    max_wait = max(wait)
    averagewait = sum(wait) / len(wait)
    # implementierung des medians benoetigt eine sortierte Liste
    for i in range(1, len(wait)):
        e = wait[i]
        j = i - 1
        while j >= 0 and e < wait[j]:
            wait[j + 1] = wait[j]
            j -= 1
        wait[j + 1] = e

    if len(wait) % 2 == 0:
        median_wait = wait[len(wait) // 2]
    else:
        median_wait = wait[len(wait) // 2 + 1]

    # with open("wartezeiten.txt", "a") as f:
    #     f.write(f"{name}\nMedian{median_wait:7}\t\tDurchschnitt{averagewait:20}\tMaximum{max_wait:20}\n\n")
    print(
        f"{name}\nMedian{median_wait:7}\t\tDurchschnitt{averagewait:20}\tMaximum{max_wait:7}\n"
    )
    return median_wait, averagewait, max_wait


def first_come_first_serve(start, work, iterations, Zeit):
    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)

    for n in range(iterations):
        Zeit = simulation(0, time_of_order, order_duration, wait, Zeit)

    return wait_results(wait, first_come_first_serve.__name__)


def shortest_job_next(start, work, iterations, Zeit):
    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)
    for j in range(iterations):
        x = 0
        for i in range(len(time_of_order)):
            if time_of_order[i] > Zeit:
                x = i
                break
        else:
            x = len(time_of_order)

        n = 0
        for i in range(x):
            if order_duration[i] < order_duration[n]:
                n = i
        Zeit = simulation(n, time_of_order, order_duration, wait, Zeit)

    return wait_results(wait, shortest_job_next.__name__)


def highest_response_ratio_next(start, work, iterations, Zeit):
    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)
    for j in range(iterations):
        x = 0
        for i in range(len(time_of_order)):
            if time_of_order[i] > Zeit:
                x = i
                break
        else:
            x = len(time_of_order)

        n = 0
        for i in range(x):
            if (
                1 + (Zeit - time_of_order[i]) / order_duration[i]
                > 1 + (Zeit - time_of_order[n]) / order_duration[n]
            ):
                n = i
        Zeit = simulation(n, time_of_order, order_duration, wait, Zeit)

    return wait_results(wait, highest_response_ratio_next.__name__)


if __name__ == "__main__":
    main()
