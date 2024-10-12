import flickrapi
import urllib.request
import os

# Set the API from flicker
api_key = 'your_key'
api_secret = 'your key'

# Set the search term and the folder name
search_term = 'your term'
folder_name = f'scrape_{search_term}'

# Create the folder if it does not exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Instantiate the Flickr API object
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Search for photos using the search term
photos = flickr.photos.search(text=search_term, per_page=500)  

# Loop through each photo
for photo in photos['photos']['photo']:
    photo_url = f'https://farm{photo["farm"]}.staticflickr.com/{photo["server"]}/{photo["id"]}_{photo["secret"]}.jpg'
    photo_file = photo_url.split('/')[-1]
    photo_path = os.path.join(folder_name, photo_file)
    urllib.request.urlretrieve(photo_url, photo_path)

# Print a message when done
print(f'Downloaded {len(photos["photos"]["photo"])} images of {search_term} and saved them in {folder_name}')
