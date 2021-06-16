import os
import re
import csv
import sys
import json
import time

from googleapiclient import discovery

def get_video_id(video_url):
    result = re.search('https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?.*v=|youtu\.be\/)([\w-]+)', video_url)
    return result.group(1) if result else None

def run_comment_scraper(video_id, amount):
    with open('config.json') as config_file:
        config = json.load(config_file)

    client = discovery.build('youtube', 'v3', developerKey=config['API_KEY'])

    with open('data.csv', 'w', encoding='utf-8', newline='') as data_file:
        writer = csv.writer(data_file)

        writer.writerow([
            'id',
            'text_original',
            'author_display_name',
            'author_channel_id',
            'like_count',
            'published_at',
            'updated_at',
            'total_reply_count',
            'is_public'
        ])

        total_count = 0
        next_page_token = ''

        while total_count < amount:
            amount_left = amount - total_count
            max_results = 20 if amount_left > 20 else amount_left

            response = None

            if next_page_token != '':
                response = client.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=max_results,
                    pageToken=next_page_token,
                    textFormat='plainText'
                ).execute()
            else:
                response = client.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=max_results,
                    textFormat='plainText'
                ).execute()

            current_count = len(response['items'])
            #reported_count = response['pageInfo']['totalResults']

            total_count = total_count + current_count

            print(f'[+] Scraped {current_count} comment(s)') # (API reported {reported_count})')

            for item in response['items']:
                snippet = item['snippet']
                comment = snippet['topLevelComment']

                comment_snippet = comment['snippet']

                writer.writerow([
                    comment['id'],
                    comment_snippet['textOriginal'].replace('\n', ' '),
                    comment_snippet['authorDisplayName'],
                    comment_snippet['authorChannelId']['value'],
                    comment_snippet['likeCount'],
                    comment_snippet['publishedAt'],
                    comment_snippet['updatedAt'],
                    snippet['totalReplyCount'],
                    snippet['isPublic']
                ])
            
            if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
                #time.sleep(5)
            else:
                print('[-] Warning: nextPageToken not reported by the API. Waiting...')
                next_page_token = ''
                time.sleep(10)

        print(f'[+] Finished, a total of {total_count} comment(s) were scraped')

if __name__ == '__main__':  
    if len(sys.argv) != 3:
        print(f'[-] Usage: {sys.argv[0]} [amount to scrape] [video id/url]')
    elif not os.path.isfile('config.json'):
        print('[-] config.json is missing')
    else:
        amount = int(sys.argv[1])
        video_id = get_video_id(sys.argv[2])

        if not video_id:
            print('[-] Invalid video url')
        elif amount < 1:
            print('[-] Invalid amount')
        else:
            run_comment_scraper(video_id, amount)
