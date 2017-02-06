from embedly import Embedly

from chappy.config import Config

client = Embedly(app.config['KEY'])

def get_video_info(video_url):
    data = client.extract(video_url)
    data_dict = {
        'video_source': data.get('provider_display'),
        'video_length': data.get('media').get('duration'),
        'video_html': data.get('media').get('html')
    }
    return data_dict

def get_img_info(img_url):
    client.extract(img_url)
    data_dict = {
        'img_height': data.get('media').get('height'),
        'img_width': data.get('media').get('width'),
        'img_html': data.get('media').get('url')
    }
    return data_dict
