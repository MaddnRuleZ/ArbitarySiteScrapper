import Utilities
from ArbitaryScrapper import ArbitaryScrapper
from MSSQLDatabase import MSSQLDatabase

testingUrl = "https://www.arius.de/de/home.html"
testingUrl2 = "http://www.argelith.com/"
testingUrl3 = "https://austing.de/"
testingUrl4 = "http://aviretta.com/"


def main():
    scrapp_eggers()
    '''print("Main")
    msql = MSSQLDatabase()
    list = msql.read_excel_column_by_index("dox/RestaurantBarMk1.xlsx", "Sheet1", 6)
    for item in list:
        print(item)'''

def scrapp_eggers():
    print("Starting Scrapping Process")
    msql = MSSQLDatabase()
    links = Utilities.read_text_file("dox/TestSet.txt")

    for url in links:
        if not url or url == "None" or url == "nan":
            print("Skipping None Type!")
            continue

        try:
            arbitary = ArbitaryScrapper(url)
            result = arbitary.get_all_matching_links()
            print("---- FINAL RESULT ------")
            print(result)
            print("----------------------")
        except:
            print("FATAL ERROR IN URL")



def production():
    print("Starting Scrapping Process")
    msql = MSSQLDatabase()
    links = Utilities.read_text_file("dox/database.txt")
    links = Utilities.remove_first_n_elements(links, 1116)

    for url in links:
        if not url or url == "None" or url == "nan":
            print("Skipping None Type!")
            continue

        try:
            arbitary = ArbitaryScrapper(url)
            result = arbitary.get_all_matching_links()

            print("---- FINAL RESULT ------")
            print(result.to_csv())
            msql.add_new_colums(result)
            print("----------------------")
        except:
            print("FATAL ERROR IN URL")

main()
















