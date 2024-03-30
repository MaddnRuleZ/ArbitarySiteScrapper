import Utilities
from ArbitaryScrapper import ArbitaryScrapper
from ExcelUtils import ExcelUtils
from MSSQLDatabase import MSSQLDatabase

href = "https://bayos.eatbu.com/?lang=de#contact"

def testing_href_curls():
    arbitary = ArbitaryScrapper(href)
    result = arbitary.get_all_matching_links()
    print(result)
def testing_Excel_Stuff():
    print("Exc")

    for x in range(1, 10):
        print("late")


def main():
    scrapp_eggers()

def scrapp_eggers():
    print("Starting Scrapping Process")
    msql = MSSQLDatabase()
    xlsx = ExcelUtils("dox/RestaurantBarMk1.xlsx", "Sheet1")

    url_list = msql.read_excel_column_by_index("dox/RestaurantBarMk1.xlsx", "Sheet1", 6)
    print("Read Document fully")

    for index, url in enumerate(url_list, start=2):
        url_string = str(url)
        print("Scrapping url :" + url_string)

        if not url_string or url_string == "None" or url_string == "nan":
            print("Skipping None Type!")
            continue

        try:
            arbitary = ArbitaryScrapper(url_string)
            result = arbitary.get_all_matching_links()
            print(f"---- RESULT for URL {index} ------")
            print(result)
            if result is None:
                continue

            xlsx.change_cell_content("N", index, result)
            print("inserted Entry")
            print("----------------------")

        except Exception as e:
            print(f"FATAL ERROR IN URL {index}: {str(e)}")


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
















