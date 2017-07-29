import urllib2
import os.path

pre_path = '../resources/'
max_size = 1500000


def download(url, folder):
    file_name = url.split('/')[-1].split('?')[0]
    full_path = pre_path + folder + '/' + file_name
    if not os.path.isfile(full_path):
        try:
            file = urllib2.urlopen(url)
            size = int(file.headers["Content-Length"])
            if size < max_size:
                with open(full_path, 'wb') as output:
                    output.write(file.read())
                    return True
            else :
                return False
        except:
            return False
