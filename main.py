import Utilities
import threading

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



def scrapp_eggers_thread(url_list, start_index, end_index):
    print("Starting Scrapping Process")
    msql = MSSQLDatabase()
    xlsx = ExcelUtils("dox/RestaurantBarMk1.xlsx", "Sheet1")

    for index, url in enumerate(url_list[start_index:end_index], start=start_index+1):
        # bruh oops
        if index < 600:
            continue

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
            if result is None or result == "":
                continue

            xlsx.change_cell_content("N", index, result)
            print("Inserted Entry")
            print("----------------------")

        except Exception as e:
            print(f"FATAL ERROR IN URL {index}: {str(e)}")

def start_multi_threaded_scrapping(url_list, num_threads=4):
    total_urls = len(url_list)
    chunk_size = total_urls // num_threads

    threads = []
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_threads - 1 else total_urls
        thread = threading.Thread(target=scrapp_eggers_thread, args=(url_list, start_index, end_index))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def main():
    msql = MSSQLDatabase()
    url_list = msql.read_excel_column_by_index("dox/RestaurantBarMk1.xlsx", "Sheet1", 6)

    print("Read Document fully")
    start_multi_threaded_scrapping(url_list, num_threads=4)


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




if __name__ == "__main__":
    main()