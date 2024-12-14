import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.ticker import MaxNLocator

large = 'Database/seasons_large.json'
LARGE: dict
with open(large, 'r') as file:
    LARGE = json.load(file)


def print_time(days):
    hour = (days-int(days))*24
    minute = (hour-int(hour))*60
    seconds = (minute-int(minute))*60
    return f'{int(days)} days - {int(hour)}h {int(minute)}m {int(seconds)}s'


Seasons = dict()
Seasons['Winter'] = []
Seasons['Spring'] = []
Seasons['Summer'] = []
Seasons['Autumn'] = []
Seasons['Year'] = []

for k, v in LARGE.items():
    Seasons['Winter'].append(v['Winter']['duration'])
    Seasons['Spring'].append(v['Spring']['duration'])
    Seasons['Summer'].append(v['Summer']['duration'])
    Seasons['Autumn'].append(v['Autumn']['duration'])
    Seasons['Year'].append(v['duration'])

days = (sum(Seasons['Year'])/len(Seasons['Year']))/86400
avgYear = print_time(days)
avgSeason = print_time(days/4)


def year_graph(what=['Year']):
    X = []
    for k in LARGE.keys():
        X.append(int(k))

    for k, v in Seasons.items():
        if k in what:
            Y = [i for i in v]
            average = np.mean(Y)

            if k == 'Year':
                unit = 'MINUTES'
                Y = [(i-average)/60 for i in Y]
            else:
                avgSpecificSeason = print_time((sum(Y)/len(Y))/86400)
                unit = 'HOURS'
                Y = [(i-average)/3600 for i in Y]

            average = np.mean(Y)

            # Kreiranje grafika
            plt.figure(figsize=(10, 6))
            # Prikaz podataka
            plt.plot(X, Y, label=f"Deviation ({unit})", color='blue')
            plt.plot(X, [average] * len(X), color='red', linestyle='-')

            plt.gca().xaxis.set_major_locator(
                MaxNLocator(integer=True, prune='lower', nbins=30))
            plt.gca().yaxis.set_major_locator(
                MaxNLocator(integer=True, prune='lower', nbins=20))

            # Postavke grafika
            plt.title(f"Changes in duration of Astronomical {k}{'' if k == 'Year' else ' on Northern Hemisphere'}\n{\
                'Mean Year: ' if k == 'Year' else 'Mean Quater of Year: '}{avgSpecificSeason if k != 'Year' else avgYear}", fontsize=16)
            plt.xlabel(f"Year", fontsize=14)
            plt.ylabel(f"Deviation from mean Year in {unit}", fontsize=14)
            plt.xlim(min(X), max(X))
            plt.ylim(min(Y)+min(Y)*0.01, max(Y)+max(Y)*0.01)

            plt.tight_layout()


def seasons_graph():
    X = [int(k) for k in LARGE.keys()]

    # Kreiranje grafikona sa zajedničkom Y-osom
    plt.figure(figsize=(10, 6))

    season = dict()
    for k in Seasons.keys():
        if k != 'Year':
            season[k] = [i/3600 for i in Seasons[k]]

    Y = season['Winter'] + season['Spring'] + \
        season['Summer'] + season['Autumn']
    average = np.mean(Y)

    for k in season.keys():
        season[k] = [i - average for i in season[k]]

    Y = season['Winter'] + season['Spring'] + \
        season['Summer'] + season['Autumn']
    average = np.mean(Y)

    plt.plot(X, season['Winter'], label="Winter", color='blue')
    plt.plot(X, season['Spring'], label="Spring", color='green')
    plt.plot(X, season['Summer'], label="Summer", color='yellow')
    plt.plot(X, season['Autumn'], label="Autumn", color='red')

    plt.axhline(y=average, color='silver', linestyle='-',
                label=f"Average: {average:.0f} hours")

    # Podesite osovinu i postavke grafikona
    plt.gca().xaxis.set_major_locator(
        MaxNLocator(integer=True, prune='lower', nbins=30))
    plt.gca().yaxis.set_major_locator(
        MaxNLocator(integer=True, prune='lower', nbins=20))

    # Postavke grafika
    plt.title(f"Changes in duration of Astronomical Seasons on Northern Hemisphere\nMean Quarter of the Year: {\
              avgSeason}", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel(f"Deviation from mean Quarter in HOURS", fontsize=14)
    plt.xlim(min(X), max(X))
    plt.ylim(min(Y)+min(Y)*0.01, max(Y)+max(Y)*0.01)

    plt.legend()
    plt.tight_layout()


seasons_graph()
# year_graph(['Year','Summer','Autumn','Spring','Winter'])
year_graph()
plt.show()
