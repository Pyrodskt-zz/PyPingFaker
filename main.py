# This is a sample Python script.
import random
import subprocess
import time
import re
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from os import system
from random import Random

clear = lambda: system('cls')


def req_time_out(mylist):
    mylist.append(['lost', 'lost', 'lost', 'lost'])
    print("Délai d\'attente de la demande dépassé.")


def reply(mylist, ip, bytes, time_down, time_up, ttl):
    rand = random.randrange(int(time_down), int(time_up))
    mylist.append([ip, bytes, rand, ttl])
    print(f"Réponse de {ip}: octets={bytes} temps={rand} ms TTL={ttl}")
    time.sleep(rand / 1000)


def command(ip, nb_occur):
    print(f"C:\WINDOWS\system32>ping -n {nb_occur} {ip}\n")


def get_ttl(ip):
    result = subprocess.Popen(f"ping -n 1 {ip}", shell=True, stdout=subprocess.PIPE)
    res = str(result.stdout.read().lower())
    print(res)
    pattern_ttl = "ttl"
    ttl = res.find(pattern_ttl)
    pat = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s')
    iip = re.findall(pat, res)[0].split()
    ttl = res[ttl + 4:ttl + 7]
    return ttl, iip[0]


def stats(ip, sent, receiv, lost, ti_max, ti_min, ti_moy):
    per_lost = (lost / (sent + receiv + lost)) * 100
    print(f'\nStatistiques Ping pour {ip}:')
    print(f'    Paquets : envoyés = {sent}, reçus = {receiv}, perdus = {lost} (perte {int(per_lost)}%) ')
    print(f"Durée approximative des boucles en millisecondes :")
    print(f'    Minimum = {ti_min}ms, Maximum = {ti_max}ms, Moyenne = {int(ti_moy)}ms')
    print('')


def main_menu():
    print("Welcome to ping faker please select the target : ")
    ip = input()
    print("Please select the minimum of ping (in ms) : ")
    ti_min = input()
    print("PLeaser select the maximum of ping (in ms) : ")
    ti_max = input()
    print('How many request you wanna fake ? (1, 2, 3, ..., 999) : ')
    nb = input()

    print(f"ip :{ip} | min time: {ti_min} | max time: {ti_max} | Nb Request to send : {nb}")
    return ip, ti_min, ti_max, nb


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rand_timeout = int(random.randrange(0, 10))
    ip, ti_min, ti_max, nb = main_menu()
    ttl, real_ip = get_ttl(ip)

    clear()
    command(ip, nb)
    mylist = []
    i = 0
    print(f'\nEnvoi d\'une requête \'ping\' [{real_ip}] avec 32 octets de données :')
    while i < int(nb):
        reply(mylist, real_ip, 32, ti_min, ti_max, ttl)
        i += 1
        if i % rand_timeout != 0:
            i += 1
            req_time_out(mylist)
            time.sleep(1)
            continue
    lost = 0
    ti_min = 0
    ti_max = 0
    sent = 0
    receiv = 0
    ti_moy = 0
    for l in mylist:
        sent += 1
        if l[0] == 'lost':
            lost += 1
        if l[0] != 'lost':
            if ti_min == 0:
                ti_min = l[2]
            ti_min = min(ti_min, l[2])
            ti_max = max(ti_max, l[2])

            receiv += 1
            ti_moy += l[2]

    ti_moy = ti_moy / (sent - lost)
    stats(real_ip, sent, receiv, lost, ti_max, ti_min, ti_moy)
    print('C:\WINDOWS\system32>')
