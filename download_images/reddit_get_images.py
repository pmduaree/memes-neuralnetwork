import requests
import oauth
import download_image
import os


def create_folders():
    if not os.path.exists('../resources'):
        os.makedirs('../resources')
    if not os.path.exists('../resources/memes'):
        os.makedirs('../resources/memes')
    if not os.path.exists('../resources/non_memes'):
        os.makedirs('../resources/non_memes')
    if not os.path.exists('../resources/data'):
        os.makedirs('../resources/data')


def is_image(image):
    url = image['url']
    extension = url.split('.')[-1].split('?')[0]
    return extension == 'jpg' or extension == 'png' or extension == 'jpeg'


def main():
    subreddits = [
        {'name': 'dankMemes', 'folder': 'memes'},
        {'name': 'memeEconomy', 'folder': 'memes'},
        {'name': 'prequelMemes', 'folder': 'memes'},
        {'name': 'meirl', 'folder': 'memes'},
        {'name': 'AdviceAnimals', 'folder': 'memes'},
        {'name': 'wholesomememes', 'folder': 'memes'},
        {'name': 'memes', 'folder': 'memes'},
        {'name': 'BikiniBottomTwitter', 'folder': 'memes'},
        {'name': 'pics', 'folder': 'non_memes'},
        {'name': 'aww', 'folder': 'non_memes'},
        {'name': 'funny', 'folder': 'non_memes'},
        {'name': 'gaming', 'folder': 'non_memes'},
        {'name': 'oldSchoolCool', 'folder': 'non_memes'},
        {'name': 'comics', 'folder': 'non_memes'},
        {'name': 'madlads', 'folder': 'non_memes'},
        {'name': 'BlackPeopleTwitter', 'folder': 'non_memes'},
        {'name': 'hmmm', 'folder': 'non_memes'}
    ]

    total_images_downloaded = 0

    create_folders()

    headers = oauth.log_in_and_get_headers()
    for subreddit in subreddits:
        subreddit_name = subreddit['name']
        folder = subreddit['folder']
        images_downloaded = 0
        count = 0
        last_name = 0
        print 'started with ' + subreddit_name

        while last_name is not None:
            after = '' if last_name == 0 else last_name
            data = {"show": 'all', "after": after, "count": count, "limit": "100"}
            response = requests.get("https://oauth.reddit.com/r/" + subreddit_name + "/new", headers=headers,
                                    params=data)
            data_got = response.json()['data']
            children = map(lambda children_response: children_response['data'], data_got['children'])
            children_only_images = filter(is_image, children)

            count += len(children)

            for children_only_image in children_only_images:
                if download_image.download(children_only_image['url'], folder):
                    images_downloaded += 1

            last_name = data_got['after']

        print 'finished with ' + subreddit_name
        print 'images downloaded ' + str(images_downloaded)
        print ''
        total_images_downloaded += images_downloaded

    print 'total images downloaded so far: ' + str(total_images_downloaded)
    print '--------------------------------'


if __name__ == "__main__":
    main()
