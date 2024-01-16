import os
import requests
from urllib.parse import urlparse

def extract_broadcast_id(input_str):
    # Extract broadcast ID from the input string (either URL or ID)
    parsed_url = urlparse(input_str)
    path_segments = parsed_url.path.split('/')
    if path_segments[-2] == 'broadcasts':
        return path_segments[-1]
    else:
        return input_str

def download_broadcast(broadcast_id):
    # Make the request to the broadcast API
    broadcast_url = f'https://api.twitter.com/1.1/broadcasts/show.json?ids={broadcast_id}'
    response_broadcast = requests.get(broadcast_url)

    # Check if the request to the broadcast API was successful
    if response_broadcast.status_code == 200:
        # Extract relevant information from the broadcast API response
        broadcast_data = response_broadcast.json()['broadcasts'][broadcast_id]

        # Create a folder with the ID from the broadcast API
        folder_name = broadcast_data['id']
        os.makedirs(folder_name, exist_ok=True)

        # Save the API response details in a text file
        api_details_file = os.path.join(folder_name, 'api_details.txt')
        with open(api_details_file, 'w') as f:
            f.write(str(broadcast_data))

        # Extract media_key from the broadcast API response
        media_key = broadcast_data['media_key']

        # Make the request to download the no redirect M3U8 playlist
        live_stream_url = f'https://api.twitter.com/1.1/live_video_stream/status/{media_key}.json'
        response_live_stream = requests.get(live_stream_url)

        # Check if the request to the live stream API was successful
        if response_live_stream.status_code == 200:
            live_stream_data = response_live_stream.json()

            # Extract relevant information from the live stream API response
            source = live_stream_data.get('source', {})
            no_redirect_playback_url = source.get('noRedirectPlaybackUrl', '')

            # Extract the original file name from the URL
            file_name = os.path.basename(urlparse(no_redirect_playback_url).path)

            # Make a request to download the M3U8 playlist
            m3u8_response = requests.get(no_redirect_playback_url)

            # Save the M3U8 file in the created folder with the original file name
            m3u8_file = os.path.join(folder_name, file_name)
            with open(m3u8_file, 'wb') as f:
                f.write(m3u8_response.content)

            print(f"API details and M3U8 file downloaded successfully in folder: {folder_name}")

        else:
            print(f"Error retrieving live stream status: {response_live_stream.status_code}")

    else:
        print(f"Error retrieving broadcast data: {response_broadcast.status_code}")

# Introduction
print("Welcome to the Twitter Broadcast Downloader!")
print("This script allows you to download Twitter broadcast details and the associated M3U8 file.")
print("You can input either the Twitter Broadcast URL or ID directly.")

# How-to explanation
print("\nHow to use:")
print("1. To get the Broadcast ID, visit the Twitter broadcast URL and extract it from the end of the URL.")
print("   Example URL: 'https://twitter.com/i/broadcasts/id_here_example'")
print("   Broadcast ID: 'id_here_example'")
print("2. Input the Twitter Broadcast URL or ID when prompted.")

# Input for the Twitter broadcast URL or ID
input_str = input("\nEnter the Twitter Broadcast URL or ID: ")
broadcast_id_input = extract_broadcast_id(input_str)

if broadcast_id_input:
    download_broadcast(broadcast_id_input)
else:
    print("Invalid Twitter Broadcast URL or ID. Please make sure the input is in the correct format.")
