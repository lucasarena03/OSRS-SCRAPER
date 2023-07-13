import requests
import random
from bs4 import BeautifulSoup

URL = "https://oldschool.runescape.wiki/w/Goblin"

def main() -> None:
    random.seed()

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    target = soup.find(id="mw-content-text")

    drops = target.find_all("table", class_="item-drops")

    drop_map = {}

    for drop in drops:
        body = drop.find("tbody")

        item_data = body.find_all("td")
        index = 0
        curr_item = ""

        while index < len(item_data):
            item = item_data[index]

            if item.has_attr("class") and item["class"] == ["item-col"]:
                curr_item = item.find("a").text
                quantity = item_data[index + 1].text
                
                if quantity == "N/A":
                    quantity = "0"
                
                rate = item_data[index + 2].text
                if rate == "Always":
                    rate = "1/1"
                elif "[" in rate:
                    rate = rate.split("[")[0]
                
                if ";" in rate:
                    rate =  rate.split(";")[0]
                    print(rate)
                
                rate = rate.replace(",", "")
                
                rtokens = rate.split("/")
                rate = float(rtokens[0]) / float(rtokens[1])
                
                drop_map[curr_item] = {
                    "quantity": quantity,
                    "rate": rate
                }
                index += 3
            else:
                index += 1
        
    print("Welcome to the OSRS drop simulator!")
    print("You are currently killing Goblins, enter an amount: ")
    amount = int(input())
    print("You are killing " + str(amount) + " Goblins.")

    drop_list = list(drop_map.keys())

    drops = []


    while len(drops) < amount:
        drop = random.choice(drop_list)
        if random.random() < drop_map[drop]["rate"]:
            drops.append(drop)
        

    for drop in drops:
        print(drop)

    
if __name__ == '__main__':
    main()