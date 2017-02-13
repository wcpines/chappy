from embedly import Embedly

from chappy.config import Config

client = Embedly(Config.EMBEDLY_API_KEY)

def get_video_metadata(video_url):
    data = client.extract(video_url)
    data_dict = {
        'source': data.get('provider_display'),
        'length': data.get('media').get('duration'),
        'html': data.get('media').get('html')
    }
    return data_dict

def get_img_metadata(img_url):
    data = client.extract(img_url)
    data_dict = {
        'height': data.get('media').get('height'),
        'width': data.get('media').get('width'),
    }
    return data_dict
