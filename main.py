import os
import requests
from urllib.parse import urlparse

def extract_broadcast_id(input_str):
    
    parsed_url = urlparse(input_str)
    path_segments = parsed_url.path.split('/')
    if path_segments[-2] == 'broadcasts':
        return path_segments[-1]
    else:
        return input_str

def download_broadcast(broadcast_id):
    
    broadcast_url = f'https://api.twitter.com/1.1/broadcasts/show.json?ids={broadcast_id}'
    response_broadcast = requests.get(broadcast_url)


    if response_broadcast.status_code == 200:
        
        broadcast_data = response_broadcast.json()['broadcasts'][broadcast_id]

        
        folder_name = broadcast_data['id']
        os.makedirs(folder_name, exist_ok=True)

        
        api_details_file = os.path.join(folder_name, 'api_details.txt')
        with open(api_details_file, 'w') as f:
            f.write(str(broadcast_data))

        
        media_key = broadcast_data['media_key']

        
        live_stream_url = f'https://api.twitter.com/1.1/live_video_stream/status/{media_key}.json'
        response_live_stream = requests.get(live_stream_url)

        
        if response_live_stream.status_code == 200:
            live_stream_data = response_live_stream.json()

            
            source = live_stream_data.get('source', {})
            no_redirect_playback_url = source.get('noRedirectPlaybackUrl', '')

            
            file_name = os.path.basename(urlparse(no_redirect_playback_url).path)

            
            m3u8_response = requests.get(no_redirect_playback_url)

            
            m3u8_file = os.path.join(folder_name, file_name)
            with open(m3u8_file, 'wb') as f:
                f.write(m3u8_response.content)

            print(f"API details and M3U8 file downloaded successfully in folder: {folder_name}")

        else:
            print(f"Error retrieving live stream status: {response_live_stream.status_code}")

    else:
        print(f"Error retrieving broadcast data: {response_broadcast.status_code}")


print("Welcome to the Twitter Broadcast Downloader!")
print("This script allows you to download Twitter broadcast details and the associated M3U8 file.")
print("You can input either the Twitter Broadcast URL or ID directly.")

print("\nHow to use:")
print("1. To get the Broadcast ID, visit the Twitter broadcast URL and extract it from the end of the URL.")
print("   Example URL: 'https://twitter.com/i/broadcasts/123456789'")
print("   Broadcast ID: '123456789'")
print("2. Input the Twitter Broadcast URL or ID when prompted.")


input_str = input("\nEnter the Twitter Broadcast URL or ID: ")
broadcast_id_input = extract_broadcast_id(input_str)

if broadcast_id_input:
    download_broadcast(broadcast_id_input)
else:
    print("Invalid Twitter Broadcast URL or ID. Please make sure the input is in the correct format.")
