import Utilities
import multiprocessing

from ArbitaryScrapper import ArbitaryScrapper
from ExcelUtils import ExcelUtils
from MSSQLDatabase import MSSQLDatabase

href = "https://bayos.eatbu.com/?lang=de#contact"

def testing_href_curls():
    arbitary = ArbitaryScrapper(href)
    result = arbitary.get_all_matching_links()
    print(result)


def scrapp_eggers(url_index_pair):
    index, url = url_index_pair
    url_string = str(url)
    print("Scrapping url :" + url_string)

    if not url_string or url_string == "None" or url_string == "nan":
        print("Skipping None Type!")
        return
    result = "None"

    try:
        arbitary = ArbitaryScrapper(url_string)
        result = arbitary.get_all_matching_links()
        print(f"---- RESULT for URL {index} ------")
        print(result)

    except Exception as e:
        print(f"FATAL ERROR IN URL {index}: {str(e)}")

    Utilities.append_string_to_file("dox/database.txt", "[" + str(index) + "]" + result)
    print("Inserted Entry")
    print("----------------------")


def main():
    msql = MSSQLDatabase()
    url_list = msql.read_excel_column_by_index("dox/RestaurantBarMkTesting.xlsx", "Sheet1", 6)
    print(len(url_list))
    print("Read Document fully")

    with multiprocessing.Pool(processes=5) as pool:
        # Use enumerate to get both index and URL
        url_index_pairs = list(enumerate(url_list, start=2))

        chunk_size = 5  # Number of processes to start concurrently
        for i in range(0, len(url_index_pairs), chunk_size):
            # Divide the list into chunks
            chunk = url_index_pairs[i:i + chunk_size]
            # Start processes asynchronously for the current chunk
            processes = [pool.apply_async(scrapp_eggers, args=(pair,)) for pair in chunk]
            # Wait for both processes in the current chunk to finish
            for process in processes:
                process.get()


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