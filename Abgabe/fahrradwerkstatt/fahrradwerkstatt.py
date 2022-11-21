import copy


def main():
    # Einlesen der Eingabedatei
    with open("beispiel0.txt", "r") as f:
        file = f.read()

    # Auftragszeit und Eingangszeit jeweils in Liste
    all_time_of_orders = [int(s) for s in file.split()[::2]]
    all_order_durations = [int(s) for s in file.split()[1::2]]

    iterations = len(all_time_of_orders)
    time = all_time_of_orders[0]
    # fuer den Fall, dass Auftrag ausserhalb Arbeitszeit gestellt wurde
    if time%1440 < 540:
        time += 540 - time%1440
    elif time%1440 > 1020:
        time += 1980 - time%1440

    first_come_first_serve(all_time_of_orders, all_order_durations, iterations, time)
    shortest_job_next(all_time_of_orders, all_order_durations, iterations, time)
    highest_response_ratio_next(all_time_of_orders, all_order_durations, iterations, time)

# berechnet die Wartezeit eines Auftrages und uebergibt die naechste Startzeit
def simulation(i, time_of_order, order_duration, wait, time):   
    # Zeit der Fertigstelllung
    i_duration = order_duration[i]
    work_day_left = 1020 - time%1440
    if i_duration > work_day_left:                  
        time += i_duration + (1 + ((i_duration - work_day_left)//480)) * 960
    else:
        time += i_duration
    # Wartezeit und Streichung des abgearbeiteten Auftrages
    wait.append(time - time_of_order[i])
    time_of_order.pop(i)
    order_duration.pop(i)
    # Startzeit des naechsten Auftrages
    if len(order_duration) > 0:
        time = max(time, time_of_order[0])
        if time%1440 < 540:
            time += 540 - time%1440
        elif time%1440 > 1020:
            time += 1980 - time%1440

    return time

# ermittelt die Ergebnisse
def wait_results(wait, name):

    max_wait = max(wait)
    averagewait = sum(wait)/len(wait)
    # Implementierung des Medians benoetigt eine sortierte Liste 
    for i in range(1, len(wait)): 
        e = wait[i] 
        j = i - 1 
        while j >= 0 and e < wait[j]: 
            wait[j + 1] = wait[j] 
            j -= 1      
        wait[j + 1] = e 
    # Ermittlung des Median
    if len(wait)%2 == 0:
        median_wait = wait[len(wait)//2]
    else:
        median_wait = wait[len(wait)//2 + 1]

    results = [median_wait, averagewait, max_wait]

    print(name + '\n' + str(results) + '\n')
    
    return results 
    
# FCFS-Verfahren
def first_come_first_serve(start, work, iterations, time):

    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)
    # Auftraege in Reihenfolge der Eingangszeit
    for n in range(iterations):
        time = simulation(0, time_of_order, order_duration, wait, time) 
    
    return wait_results(wait, first_come_first_serve.__name__)

# SJN-Verfahren
def shortest_job_next(start, work, iterations, time):

    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)
    # Ermittlung der Auftraege, die aktuell vorliegen
    for j in range(iterations):
        x = 0
        for i in range(len(time_of_order)):
            if time_of_order[i] > time:
                x = i
                break
        else:
            x = len(time_of_order)
        # Ermittlung des kuerzesten der vorliegenden Verfahren
        n = 0
        for i in range(x):
            if order_duration[i] < order_duration[n]:
                n = i
        time = simulation(n, time_of_order, order_duration, wait, time)
    
    return wait_results(wait, shortest_job_next.__name__)

# HRRN-Verfahren
def highest_response_ratio_next(start, work, iterations, time):

    wait = []
    time_of_order = copy.deepcopy(start)
    order_duration = copy.deepcopy(work)
    # Ermittlung der Auftraege, die aktuell vorliegen    
    for j in range(iterations):
        x = 0
        for i in range(len(time_of_order)):
            if time_of_order[i] > time:
                x = i
                break
        else:
            x = len(time_of_order)
        # Ermittlung des Verfahrens mit der hoechsten response ratio
        n = 0
        for i in range(x):
            if 1 + (time - time_of_order[i]) / order_duration[i] > 1 + (time - time_of_order[n]) / order_duration[n]:
                n = i 
        time = simulation(n, time_of_order, order_duration, wait, time)
    
    return wait_results(wait, highest_response_ratio_next.__name__)

if __name__ == "__main__":
    main()