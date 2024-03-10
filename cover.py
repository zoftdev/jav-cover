
##  use python script  scan my folder. if file name is  string-number.[mp4,avi] then search  google image for  string-number and save beside it as string-number.png
# https://cse.google.com/cse?cx=265fb1f1a6c0d4169   
# https://developers.google.com/custom-search/v1/using_rest
# echo "0 */4 * * * python3 /mnt/data/my-lib/cover.py /mnt/data/Downloads/complete/_x >> /tmp/cover.log" | crontab -
# echo "10 */4 * * * python3 /mnt/data/my-lib/cover.py  /mnt/data/my-lib/_x  >> /tmp/cover.log" | crontab -
# echo "20 */4 * * * python3 /mnt/data/my-lib/cover.py  /mnt/data/my-lib/moviex/  >> /tmp/cover.log" | crontab -
 
import os
import re
import requests
from PIL import Image
from io import BytesIO

import urllib.parse

def search_google_images(query):
    # Replace 'YOUR_API_KEY' and 'YOUR_CX' with your actual API key and CX.
    api_key = "AIzaSyDTE2MY-WdoT6NmmZoH00YUfUt4VWi4VUA"
    cx = "265fb1f1a6c0d4169"
    #url encode query
    query =  urllib.parse.quote(query)

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&searchType=image&key={api_key}&cx={cx}"
    print("search_google_images:",url)
    


    data = requests.get(url).json()
    #if hit rate limit error.code=429 then stop app
    if 'error' in data:
        print("Error:",data['error']['code'])
        if data['error']['code'] == 429:
            print("Error: hit rate limit")
            exit(429)
    
    return data['items'][0]['link'] if 'items' in data else None

def download_and_save_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(filename)
            return True
    except Exception as e:
        print(f"Error occurred while downloading and saving image: {e}")
        return False


# get only last string-number from input
#  example: getTitle("anything-123") return "anything-123"
#       getTitle("anything-xxx-123") return "xxx-123"
#       getTitle("abc-456") return "abc-456"
#       getTitle("no-number") return "no-number"
#       getTitle("050_3xplanet_NHDTA-618") return "NHDTA-618"        
def getTitle(base_name):
    title= re.sub(r".*?([a-zA-Z]+-\d+)$", r"\1", base_name)
    print("getTitle:",title)
    return title


def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            
            if re.match(r".*\.(mp4|avi|mkv)$", filename):
                
                

                base_name = os.path.splitext(filename)[0]  # Get the base name without the extension
                
                #if base_name len < 5 then skip
                if len(base_name) < 5:
                    continue

                png_filename = os.path.join(root, f"{base_name}.png")
                txt_filename = os.path.join(root, f"{base_name}-cover-not-found.txt")

                # Skip if PNG image exists or the not-found TXT file exists
                if os.path.exists(png_filename) or os.path.exists(txt_filename):
                    print(f"Skipping {base_name}, image already exists or cover not found.")
                    continue

                # Proceed to search and download the image if it doesn't exist
                #possible of  format: anything-string-number.*  then use only  string-number to search
                search_title= getTitle(base_name)
                image_url = search_google_images(search_title+" jav")
                if image_url:
                    if not download_and_save_image(image_url, png_filename):
                        with open(txt_filename, 'w') as f:
                            f.write("Error occurred while downloading and saving image.")
                        print(f"Error occurred while downloading and saving image for {base_name}, created not-found file.")
                    else:
                        print(f"Saved image for {base_name}")
                else:
                    # Optionally, create a TXT file if the image search did not yield any result
                    with open(txt_filename, 'w') as f:
                        f.write("Cover not found.")
                    print(f"Cover not found for {base_name}, created not-found file.")


if __name__ == "__main__":
    #get path from  argument
    import sys
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        process_folder(folder_path)
    else:
        print("Usage: python cover.py <folder_path>")
        print("Example: python cover.py /path/to/folder")
        sys.exit(1)