import urllib.request
from bs4 import BeautifulSoup
import csv

# starting cursor location (find this by inspect elementing the review page and 
# retrieving the value stored in the hidden input tag - userreviewscursor )
cursor = "AoJwrdOD5IADftLMuAM"

# data header
header = ["Profile Name", "Date", "Recommendation", "Review", "Hours on Record", "Found Helpful", "Profile Link"]
f = open('all_reviews.csv', 'w', encoding="utf-8", newline='')
writer = csv.writer(f)
writer.writerow(header)

# change the page range depending on the number of reviews you want to scrape
# every page contains 10 reviews
# IMPORTANT: if there are encoding snags or timeouts, restart the scrape with a new file and 
# change the cursor (above) to the next cursor location and the page (starting i) to the next indice
for i in range(2,100000):
    # change the following parameters depending on the game and language
    language = "default" #english
    appID = "570"
    with urllib.request.urlopen("https://steamcommunity.com/app/" + appID + "/homecontent/?userreviewscursor=" + cursor + "%3D&userreviewsoffset=" + str((10 * i) - 10) + "&p=" + str(i) + "&workshopitemspage=" + str(i) + "&readytouseitemspage=" + str(i) + "&mtxitemspage=" + str(i) + "&itemspage=" + str(i) + "&screenshotspage=" + str(i) + "&videospage=" + str(i) + "&artpage=" + str(i) + "&allguidepage=" + str(i) + "&webguidepage=" + str(i) + "&integratedguidepage=" + str(i) + "&discussionspage=" + str(i) + "&numperpage=10&browsefilter=mostrecent&browsefilter=mostrecent&appid=570&appHubSubSection=10&appHubSubSection=10&l=english&filterLanguage=schinese&searchText=&maxInappropriateScore=50&forceanon=1") as url:
        data = url.read().decode()
        parsed_html = BeautifulSoup(data)
        cursor = parsed_html.body.find('input', attrs={'name':'userreviewscursor'})
        cursor = str(cursor['value'])[0: len(cursor) - 1]
        if '+' in cursor:
            cursor = cursor.replace('+', '%2B')
        print("Curser Location:", cursor)
        print("Next Indice:", i + 1)
       
        scraped_users = parsed_html.body.find_all('div', attrs={'class':'apphub_Card modalContentLink interactable'})

        for review in scraped_users:
            base_term = ''
            if review.find('div', attrs={"class":"apphub_CardContentAuthorName offline ellipsis"}) != None:
                base_term = 'offline'
            elif review.find('div', attrs={"class":"apphub_CardContentAuthorName online ellipsis"}) != None:
                base_term = 'online'
            else:
                base_term = 'in-game'

            data = [review.find('div', attrs={"class":"apphub_CardContentAuthorName " + base_term + " ellipsis"}).find("a", recursive=False).text,
                review.find('div', attrs={"class":"date_posted"}).text.strip()[8:],
                review.find('div', attrs={"class":"title"}).text,
                review.find('div', attrs={"class":"apphub_CardTextContent"}).get_text().strip().replace(review.find('div', attrs={"class":"date_posted"}).text.strip(), "").strip(),
                review.find('div', attrs={"class":"hours"}).text.split(" ")[0],
                review.find('div', attrs={"class":"found_helpful"}).text.strip().replace("\t\t\t\t0", ""),
                review.find('div', attrs={"class":"apphub_CardContentAuthorName " + base_term + " ellipsis"}).find("a", recursive=False)['href']]
            
            writer.writerow(data)
f.close()