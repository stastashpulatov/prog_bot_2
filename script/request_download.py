import requests
from tqdm import tqdm



def download_file(url, filename):
    response = requests.get(url, stream=True)

    file_size = int(response.headers.get('Content-Length', 0))
    progress = tqdm(response.iter_content(1024), f'Downloading {filename}', total=file_size, unit='B', unit_scale=True,
                    unit_divisor=1024)

    with open(filename, 'wb') as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
