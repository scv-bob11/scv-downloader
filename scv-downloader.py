import argparse
from urllib.parse import urlparse

from crawler import ImmunefiCrawler


immunefi_crawler = ImmunefiCrawler()
downloader = lambda x: print(x)

def download(url):
    assets = immunefi_crawler.get_assets(url)
    downloader(assets)


def download_all():
    bounties = immunefi_crawler.get_all()
    print(bounties)


def main():
    def type_url(arg):
        url = urlparse(arg)
        if all((url.scheme, url.netloc)):
            return arg
        raise argparse.ArgumentTypeError('Invalid URL')

    parser = argparse.ArgumentParser(description='Download smart contract source code on Immunefi')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    help_man = lambda args: parser.print_help()

    one_or_all = parser.add_mutually_exclusive_group()
    one_or_all.add_argument('-a', '--all', action='store_true', help='download all bounties of Immunefi')
    one_or_all.add_argument('-u', '--url', type=type_url)

    
    args = parser.parse_args()

    if args.all:
        download_all()
    elif args.url:
        download(args.url)
    else:
        parser.print_help()
        

if __name__ == '__main__':
    main()
