from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver

START_URL ="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser=webdriver.Chrome("/Users/admin/Documents/myvenv/chromedriver")

browser.get(START_URL)
time.sleep(10)

 headers = ["name", "bayer_designation", "distance", "spectral_class", "mass","radius","luminosity"]
    planet_data = []
def scrape():
    headers = ["name", "bayer_designation", "distance", "spectral_class", "mass","radius","luminosity"]
    planet_data = []
    for i in range(0, 96):

         while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Check page number    
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
       
        for ul_tag in soup.find_all("ts", attrs={"class", "brighteststars"}):
            li_tags = ul_tag.find_all("tr")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")


        hyperlink_li_tag = li_tags[0]

            temp_list.append("https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            planets_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")

 scrape()


new_planets_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        new_planets_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

#Calling method

for index, data in enumerate(planets_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_planets_data[0:10])

final_planet_data = []

for index, data in enumerate(planets_data):
    new_planet_data_element = new_planets_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)

with open("final_1.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)