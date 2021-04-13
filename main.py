import os
import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()


def fetchData(id):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=id
    )
    response = request.execute()
    return response


def getComment(data):
    comments = data["items"]
    data = []
    for snip in comments:
        data.append(snip["snippet"]["topLevelComment"]
                    ["snippet"]["textOriginal"])
    return data


def userInsertLink():
    id = ""
    while(True):
        try:
            link = input("Insert Youtube Link: ")
            id = link.split("https://www.youtube.com/watch?v=")[1]
            break
        except:
            print("[!] Invalid Video Link")
    return id


if __name__ == "__main__":
    id = userInsertLink()
    data = fetchData(id)
    comments = getComment(data)

    for c in comments:
        print(f"Comment:\n{c}\n\n")
