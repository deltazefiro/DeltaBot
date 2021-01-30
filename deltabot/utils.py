

def get_local_proxy():
    from urllib.request import getproxies
    try:
        return getproxies()['http']
    except KeyError:
        return None


def get_xml_segment(data: str):
    from nonebot import message
    return message.MessageSegment(type_='xml', data={'data': str(data)})


def download_file(url: str, download_path: str):
    import requests, sys, os
    with open(download_path+'.downloading', 'wb') as f:
        response = requests.get(url, stream=True)
        total = int(response.headers.get('content-length'))

        downloaded = 0

        for data in response.iter_content(chunk_size=1024*10):
            downloaded += len(data)
            f.write(data)

            done = int(30 * downloaded / total)
            sys.stdout.write("\rDownloading %.2fM / %.2fM " %(downloaded/1024**2, total/1024**2)+\
                             f"[{'█' * done}{'.' * (30 - done)}]")
            sys.stdout.flush()

    sys.stdout.write('\n')
    os.rename(download_path+'.downloading', download_path)