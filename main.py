import Utilities
from ArbitaryScrapper import ArbitaryScrapper


testingUrl = "https://www.arius.de/de/home.html"
testingUrl2 = "http://www.argelith.com/"
testingUrl3 = "https://austing.de/"
testingUrl4 = "http://aviretta.com/"


def main():
    print("starting")

    for url in Utilities.read_text_file("dox/database.txt"):
        arbitary = ArbitaryScrapper(url)
        result = arbitary.get_all_matching_links()
        print(result.to_csv())









main()