import googleapiclient.discovery
import pandas as pd

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = ""  # Replace with API Key

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

## Load up to 200 pages of comments
## Can change counter to add more, but it takes very long
def load_comments(video_id):
    counter = 0
    comments = []
    next_page_token = None

    while True:  # Loop until there are no more pages
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat = "plainText"
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])

        next_page_token = response.get('nextPageToken')
        counter += 1
        print(f'Page {counter}')
        if not next_page_token:  # Break the loop if no more pages are left
            break
        if counter == 200: # Break loop at pages = counter
            break

    return comments

# Add video IDs here to grab all comments
video_list = ['eQfMbSe7F2g','ZfVYgWYaHmE','TQpwONzpcy4','2m1drlOZSDw','avz06PDqDbM','bK6ldnjE3Y0','uYPbbksJxIg','pBk4NYhWNMM','8zIf0XvoL9Y','r51cYVZWKdY','hebWYacbdvc','uwmDH12MAA4', 'iuk77TjvfmE','wS_qbDztgVY']

df_list = []

for item in video_list:
    # Use the function to load all comments for the video
    video_comments = load_comments(item)
    df = pd.DataFrame(video_comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])
    temp_name  = f"{item}.csv"
    df.to_csv(temp_name)
