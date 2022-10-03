import argparse
from tqdm import tqdm
import concurrent.futures
from urllib.parse import urlparse

from crawler import ImmunefiCrawler
from url_parser import URLParser

immunefi_crawler = ImmunefiCrawler()
downloader = lambda x: print(x)
parser = URLParser()

def run(func, arg_iter):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		results = list(tqdm(executor.map(func, arg_iter), total=len(arg_iter)))
	return results

def download(url):
	assets = immunefi_crawler.get_assets(url)
	downloader(assets)
	
	# todo
	project_name = url[url.find("bounty") + 6 :]
	print(project_name[1:-1])
	parser.parse_all(assets, "." + project_name)


def download_all(): # not thread
	bounties = immunefi_crawler.get_all()
	print(len(bounties))
	for bounty in bounties: 
		download(bounty)
	# run(immunefi_crawler.get_assets, bounties)


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

# python3 scv-downloader.py -u https://immunefi.com/bounty/lido/
# python3 scv-downloader.py -a 
