import os

import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        # parentId="UgzDE2tasfmrYLyNkGt4AaABAg"
        videoId="Z2ol5_qmvsg"
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()
