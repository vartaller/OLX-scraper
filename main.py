from bs4 import BeautifulSoup
from unidecode import unidecode
import datetime
import re
import requests
import time
import winsound

def read_offers(offers_list, n_last_offers):
    offers_names = []
    offers_links = []
    offers_loc_date = []
    i = 0
    while i < n_last_offers:
        offers_names.append(offers_list[i].find("h6").text)
        offers_links.append(offers_list[i].find("a")['href'])
        offers_loc_date.append(offers_list[i].find("p", attrs={"data-testid": "location-date"}).text)
        i += 1
    return offers_names, offers_links, offers_loc_date


def get_offers_obj_list(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    offers_list = soup.find_all("div", attrs={"data-cy": "l-card"})
    return (offers_list)


def get_loc_date(offers_loc_date_next, index_next):
    loc = re.search(', (.+?) - ', unidecode(offers_loc_date_next[index_next])).group(1)
    hours = int(re.search('\d{2}', unidecode(offers_loc_date_next[index_next])).group(0)) + hours_correction
    mins = int(unidecode(offers_loc_date_next[index_next])[-2:])
    return loc, hours, mins

def calc_diff_time(hours, mins):
    current_time = datetime.datetime.now()
    current_mins = int(current_time.minute) + int(current_time.hour) * 60
    diff_time = current_mins - mins - hours * 60
    return diff_time

def print_new_offer(loc, hours, mins, offers_links_next, index_next):
    print('NEW OFFER!', flush=True)
    print(unidecode(name_next) + ' | ' + loc + ' | ' + str(hours) + ':' + str(mins), flush=True)
    print('https://www.olx.pl' + unidecode(offers_links_next[index_next]), flush=True)
    print('NEW OFFER!', flush=True)
    winsound.PlaySound(open(song,"rb").read(), winsound.SND_MEMORY)
    input("Press Enter to continue...")

def print_prev_offers(loc, hours, mins, name_next):
    print(unidecode(name_next)[ 0 : 28 ] + ' | ' + loc[ 0 : 14 ] + '\t|' + str(hours) + ':' + str(mins), flush=True)


# ==== PARAMETERS
url = "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/krakow/?search%5Bprivate_business%5D=private&search%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D=2000"
song = "ringtone.wav"
n_last_offers = 8
time_window_new_offers = 15
time_window_all_offers = 120
hours_correction = 0
repeat_delay = 20
# ==== PARAMETERS

offers_obj_list = get_offers_obj_list(url)
offers_all, links_all, offers_loc_date_all = read_offers(offers_obj_list, 30)
offers_names_prev = []
offers_names_next = []
t = 0
n_cycle = 0
while t < 1:
    offers_obj_list = get_offers_obj_list(url)
    offers_names_prev, offers_links_prev, offers_loc_date_prev = read_offers(offers_obj_list, n_last_offers)
    time.sleep(repeat_delay)

    offers_obj_list = get_offers_obj_list(url)
    offers_names_next, offers_links_next, offers_loc_date_next = read_offers(offers_obj_list, n_last_offers)

    for index_next, name_next in enumerate(offers_names_next):
        loc, hours, mins = get_loc_date(offers_loc_date_next, index_next)
        if hours > 24:
            hours -= 24
        diff_time = calc_diff_time(hours, mins)
        if name_next not in offers_all:
            offers_all.append(name_next)
            if diff_time < time_window_new_offers:
                print_new_offer(loc, hours, mins, offers_links_next, index_next)
        else:
            if diff_time < time_window_all_offers:
                loc, hours, mins = get_loc_date(offers_loc_date_next, index_next)
                if hours > 24:
                    hours -= 24
                print_prev_offers(loc, hours, mins, name_next)
    print(unidecode(name_next)[ 0 : 28 ] + ' | ' + loc[ 0 : 14 ] + '\t|' + str(hours) + ':' + str(mins), flush=True)
    n_cycle += 1
    print('-------------------------------------', n_cycle, flush=True)
    