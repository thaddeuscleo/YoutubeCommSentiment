import io
import re
import csv
import sys
import time

from selenium import webdriver
from progress.bar import Bar

def is_youtube_video_url(video_url):
    match = re.match('https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?.*v=|youtu\.be\/)(?:[\w-]+)', video_url)
    return True if match else False

def run_comment_scraper(video_url, scroll_count):
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    driver.get(video_url)
    driver.maximize_window()
    time.sleep(5)
    
    title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
    comment_section = driver.find_element_by_xpath('//*[@id="comments"]')

    print('[+] Scrolling to comment section')

    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)

    bar = Bar('[+] Scrolling comments', max=scroll_count)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    for i in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        bar.next()

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    bar.finish()

    username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
    comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')

    print(f'[+] Saving results into results.csv ...')

    with io.open('results.csv', 'w', newline='', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
        writer.writerow(["Username", "Comment"])

        for username, comment in zip(username_elems, comment_elems):
            writer.writerow([username.text, comment.text])

    print(f'[+] Finished, a total of {len(comment_elems)} comment(s) were scraped')

    driver.close()

if __name__ == '__main__':  
    if len(sys.argv) != 3:
        print(f'[+] Usage: {sys.argv[0]} [video id/url] [scroll count]')
    else:
        video_url    = sys.argv[1]
        scroll_count = int(sys.argv[2])

        if not is_youtube_video_url(video_url):
            print('[-] Invalid video url')
        elif scroll_count < 1:
            print('[-] Invalid scroll count')
        else:
            run_comment_scraper(video_url, scroll_count)
