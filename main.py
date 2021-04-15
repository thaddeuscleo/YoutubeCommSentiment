import os
import googleapiclient.discovery
import csv
from dotenv import load_dotenv
import re

load_dotenv()


def fetch_data(video_id):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    dev_key = os.getenv("DEVELOPER_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=dev_key)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()
    return response


def remove_emoji(text):
    regex_pattern = re.compile(pattern="["
                                       u"\U0001F600-\U0001F64F"
                                       u"\U0001F300-\U0001F5FF"
                                       u"\U0001F680-\U0001F6FF"
                                       u"\U0001F1E0-\U0001F1FF"
                                       u"\U00002702-\U000027B0"
                                       u"\U000024C2-\U0001F251"
                                       "]+", flags=re.UNICODE)
    return regex_pattern.sub(r'', text)


def get_comment(collected_data):
    comments_list = collected_data["items"]
    com_list = []
    for snip in comments_list:
        user_comment = {
            "username": snip["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
            "comment": snip["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        }
        com_list.append(user_comment)
    return com_list


def user_insert_link():
    while True:
        try:
            # link = input("Insert Youtube Link: ")
            link = "https://www.youtube.com/watch?v=hQ18dK-RTR0"
            link = link.split("https://www.youtube.com/watch?v=")[1]
            break
        except TypeError:
            print("[!] Invalid Video Link")
    return link


if __name__ == "__main__":
    link_id = user_insert_link()
    data = fetch_data(link_id)
    comments = get_comment(data)

    try:
        with open("comments.csv", 'w', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["username", "comment"], delimiter=',', lineterminator='\n')
            writer.writeheader()
            for com in comments:
                writer.writerow(com)
    except IOError:
        print("Fail To Read")
