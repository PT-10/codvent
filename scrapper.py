import os
import requests
from bs4 import BeautifulSoup
import markdownify

def save_day_content(day_number):
    url = f"https://adventofcode.com/2024/day/{day_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # print(soup)
    # # Find the main div and extract the article content
    main_div = soup.find("main")
    markdown_text = markdownify.markdownify(str(main_div), heading_style="ATX")

    start_phrase = "To play, please identify yourself via one of these services:"
    if start_phrase in markdown_text:
        markdown_text = markdown_text.split(start_phrase)[0].strip()

    directory = f"d{day_number}"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "README.md")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(markdown_text.strip())

    print(f"Content for Day {day_number} saved to {file_path}")

if __name__ == '__main__':
    day_number = int(input("Enter the day number: "))
    save_day_content(day_number)