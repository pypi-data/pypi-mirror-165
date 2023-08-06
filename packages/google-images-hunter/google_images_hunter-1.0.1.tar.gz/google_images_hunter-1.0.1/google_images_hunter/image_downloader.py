import urllib.error
import urllib.request
from time import sleep

class ImageDownloader:

    def __init__(self, url_list, path : str = './'):

        self.iterator = 0
        for url in url_list:
            self.new_path = f'{path}{self.iterator}.jpeg'
            for _ in range(10):
                try:
                    with urllib.request.urlopen(url, timeout=3) as web_file:
                        data = web_file.read()
                        with open(self.new_path, mode='wb') as local_file:
                            local_file.write(data)
                            print(f'Image {self.iterator} saved')
                            break # Success on download
                except:
                     pass # Escapes URL's that don't work (probably connection refused)
            self.iterator += 1
            sleep(1)