from codebase.utils import asin_to_url
from codebase.dataset_loader import DatasetLoader
from codebase.parser.parse import parse_asin

loader = DatasetLoader()
asin_list = loader.load_dataset()
url_list = asin_to_url(asin_list)
for url in url_list[0:3]:
    parse_asin(url)