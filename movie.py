"""
Open load movies wrapper.
User can search, Select from
from a range of curated lists
like genre, year of release, featured,
top or most popular movies.
The movie is opened in the default
browser without the hassle of ads
or aanoying redirects.
The script cannot detect if the movie
at the end of the link is deleted or not

python3 movie.py -h
for more info on and arguments used.
"""
import argparse
from bs4 import BeautifulSoup as bs
import os
import requests
import textwrap
import time
from urllib.parse import unquote, urlparse
import webbrowser as wb
import youtube_dl

# Restrict choices of genre and years(1992 - current year)
genre_choices = ['action', 'adventure', 'animation',
                 'biography', 'comedy', 'crime', 'documentary', 'drama',
                 'family', 'fantasy', 'featured', 'foreign', 'history',
                 'horror', 'music', 'mystery', 'romance', 'science-fiction',
                 'short', 'tagalog-dubbed', 'thriller', 'tv-movie', 'upcoming',
                 'war', 'western']

year_choices = []
for i in range(1992, int(time.strftime("%Y"))+1):
    year_choices.append(str(i))

# Define Comamnd Line arguments
parser = argparse.ArgumentParser(description="Openload Movies wrapper")
parser.add_argument("-d", action="store_true", help="Optional flag to download \
                     if possible")
master = parser.add_mutually_exclusive_group()
user = master.add_mutually_exclusive_group()
user.add_argument("-g", nargs="?", help="Specify a genre")
user.add_argument("-y", help="Specify a release year", nargs="?")
user.add_argument("-s", help='Search a movie', nargs="*", type=str)

curated = master.add_mutually_exclusive_group()
curated.add_argument("-f", help="Featured Movies", action="store_true")
curated.add_argument("-t", help="Top Rated Movies", action="store_true")
curated.add_argument("-p", help="Popular/Most viewed Movies",
                     action="store_true")
curated.add_argument("-m", help="OpenLoad movies list", action="store_true")
args = parser.parse_args()

num_true = 0
for i in vars(args).values():
    if i:
        num_true +=1

if num_true <= 1 and args.d:
    print("Use atleast one other argument with -d option")
    quit()

# Print help if no argunment is mentioned
if not any(vars(args).values()):
    print("Atleast one of the arguments must be mentioned.\n")
    print(parser.print_help())
    quit()


# Get openload movie link.
def get_openloadmovie_link():
    url = "https://duckduckgo.com/html/?q=openload+movie"
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    for i in soup.find_all("a", attrs={"class": "result__a"}):
        if i.text == "Openload Movies - Watch Free HD Movies Online":
            return unquote(i['href']).replace("/l/?kh=-1&uddg=", "")


# Gets movie list from given URL
def get_curated_list(url):
    count = 1
    url_list = []
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    for i in soup.find_all("div", attrs={"class": "poster"}):
        try:
            title = unquote(i.img['alt'])[:-16]
        except(AttributeError):
            title = "Unknown title"
        try:
            quality = i.find("span", attrs={"class": "quality"}).text.strip()
        except(AttributeError):
            quality = "Unknown quality"
        try:
            rating = i.find("div", attrs={"class": "rating"}).text.strip()
        except(AttributeError):
            rating = "Unknown rating"
        try:
            description = soup.find("div", attrs={"class": "texto"}).text
        except:
            description = "Description not found"
        print(str(count) + "*"*50)
        print(title + "\n")
        print(textwrap.fill(description, 50))
        print("\n" + quality + " | " + rating + " stars")
        print("*"*50)
        url_list.append(i.a['href'])
        count += 1
    return url_list


# Function to search and fire movie
def search_movie(query, page):
    total_pages = 0
    url_list = []
    count = 1
    url = "https://openloadmovie.org/page/"
    term = url + str(page) + "/?s=" + query
    response = requests.get(term)
    soup = bs(response.content, "lxml")
    for i in soup.find_all("div", attrs={"class": "details"}):
        url_list.append(i.a['href'])
        print(str(count) + "*"*50 + "\n" + i.a.text)
        print(i.find("span", attrs={"class": "rating"}).text + "\n" + "*"*50)
        count += 1
    while True:
        temp = input("Enter number to watch the movie or 0 for next page or q to quit ")
        if temp[0].upper() == "Q":
            print("Thanks for using :)")
            quit()
        elif int(temp) < len(url_list) + 1 and int(temp) != 0:
            download_flag = input("Do you want to download? [Y/N] ")
            if download_flag[0].upper() == "Y":
                fire_movie(url_list[int(temp) - 1], 1)
            else:
                fire_movie(url_list[int(temp) - 1], 0)
            quit()
        elif int(temp) == 0:
            for i in soup.find_all("span", attrs={"class": ""}):
                total_pages = i.text.split("of")[1].strip()
            if not total_pages:
                print("This is the only page. Try again")
                quit()
            if int(page) < int(total_pages):
                search_movie(query, page+1)
        elif temp[0].upper() == "Q":
            print("Thanks for using :)")
            quit()
        else:
            print("Wrong choice")
            quit()

# Open browser to movie link.
def fire_movie(url, download_flag):
    print(args)
    os.system("reset")
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    direct_link = soup.find("div", attrs={"id": "option-1"}).iframe['src']
    print(direct_link)
    ydl_link = []
    ydl_link.append(direct_link)
    print(ydl_link)
    if args.d or download_flag:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(ydl_link)
    else:
        wb.open(direct_link)
    quit()


url = get_openloadmovie_link()
print(url)
if not url:
    print("URL not found...")
    print("Try after some time.")
    quit()


# Call relevant function based on arguments
# and exit on wrong input
if args.f:
    if url[-1] == "/":
        url = url + "genre/featured/page/"
    else:
        url = url + "/genre/featured/page/"
    url_list = get_curated_list(url + "1")
elif args.t:
    if url[-1] == "/":
        url = url + "top-rated/page/"
    else:
        url = url + "/top-rated/page/"
    url_list = get_curated_list(url + "1")
elif args.p:
    if url[-1] == "/":
        url = url + "most-viewed/page/"
    else:
        url = url + "/most-viewed/page/"
    url_list = get_curated_list(url + "1")
elif args.m:
    if url[-1] == "/":
        url = url + "movies/page/"
    else:
        url = url + "/movies/page/"
    url_list = get_curated_list(url + "1")
elif args.s:
    search_movie(" ".join(args.s), 1)
elif args.g:
    if args.g not in genre_choices:
        print("Select one of the following genres.")
        print(genre_choices)
        quit()
    if url[-1] == "/":
        url = url + "genre/" + args.g + "/page/"
    else:
        url = url + "/genre/" + args.g + "/page/"
    url_list = get_curated_list(url + "1")

elif args.y:
    if args.y not in year_choices:
        print("Select year between " + str(year_choices[0]) + "-" +
              str(year_choices[-1]) + " (both included)")
        quit()
    if url[-1] == "/":
        url = url + "release/" + args.y + "/page/"
    else:
        url = url + "/release/" + args.y + "/page/"
    url_list = get_curated_list(url + "1")

page_number = 2
break_count = 1
while break_count < 5 and not args.s:
    temp = input("Enter a number to load that movie or 0 to load next page or q to quit ")
    try:
        if temp[0].upper() == "Q":
            print("Thanks for using :)")
            quit()
        elif int(temp) == 0:
            os.system('reset')
            url_list = get_curated_list(url + str(page_number))
            page_number += 1
        elif int(temp) < len(url_list) + 1 and int(temp) != 0:
            download_flag = input("Do you want to download? [Y/N] ")
            if download_flag[0].upper() == "Y":
                fire_movie(url_list[int(temp) - 1], 1)
            else:
                fire_movie(url_list[int(temp) - 1], 0)
            break_count = 10
        else:
            break_count += 1
    except Exception as e:
        print("\nWrong choice")
        print("Enter 0 for next page or the number of the movie to watch\n")
        break_count += 1
if break_count == 5:
    print("You've bored me with wrong choices")
    print("I give up. Try again later")

quit()
