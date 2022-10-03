from scanner_downloader import ScannerDownloader
from git_downloader import GitDownloader

class URLParser:
	def __init__(self):
		self.scanner_downloader = ScannerDownloader()
		self.git_downloader = GitDownloader()
		self.GITHUB = "github"
		self.ETHSCAN = "etherscan"
		self.BSCSCAN = "bscscan"
		self.AURSCAN = "aurorascan"
		self.POLSCAN = "polygonscan"
		self.FANSCAN = "ftmscan"
		self.ARBSCAN = "arbiscan"
		self.MOOSCAN = "moonscan"
		self.SNOSCAN = "snowtrace"
		self.OPTSCAN = "optimistic"

	def extract_contract_addr(self, url: str):
		start_idx = url.find("0x")
		return url[start_idx:start_idx + 42]

	def parse(self, url: str, base_folder = "."):
		if self.GITHUB in url:
			self.git_downloader.download(base_dir=base_folder, url=url)
			return

		if self.OPTSCAN in url: # eth보다 먼저 있어야 함
			self.scanner_downloader.downloader("OPT", self.extract_contract_addr(url), base_folder, False)
			return
		if self.ETHSCAN in url:
			self.scanner_downloader.downloader("ETH", self.extract_contract_addr(url), base_folder, False)
			return
		if self.BSCSCAN in url:
			self.scanner_downloader.downloader("BSC", self.extract_contract_addr(url), base_folder, False)
			return
		if self.AURSCAN in url:
			self.scanner_downloader.downloader("AUR", self.extract_contract_addr(url), base_folder, False)
			return
		if self.POLSCAN in url:
			self.scanner_downloader.downloader("POL", self.extract_contract_addr(url), base_folder, False)
			return
		if self.FANSCAN in url:
			self.scanner_downloader.downloader("FAN", self.extract_contract_addr(url), base_folder, False)
			return
		if self.ARBSCAN in url:
			self.scanner_downloader.downloader("ARB", self.extract_contract_addr(url), base_folder, False)
			return
		if self.MOOSCAN in url:
			self.scanner_downloader.downloader("MOO", self.extract_contract_addr(url), base_folder, False)
			return
		if self.SNOSCAN in url:
			self.scanner_downloader.downloader("SNO", self.extract_contract_addr(url), base_folder, False)
			return

	def parse_all(self, urls: list, base_folder = "."):
		for url in urls:
			self.parse(url, base_folder)



if __name__ == '__main__':
	
	# url = "https://etherscan.io/address/0x4F4495243837681061C4743b74B3eEdf548D56A5"
	# url = "https://etherscan.io/address/0x4Fabb145d64652a948d72533023f6E7A623C7C53"
	# url = "https://bscscan.com/address/0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
	# url = "https://polygonscan.com/address/0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
	# url = "https://aurorascan.dev/address/0x0294f2ca320097e098d373d266b21891c3df6a07"
	# url = "https://ftmscan.com/address/0xe1146b9ac456fcbb60644c36fd3f868a9072fc6e"
	# url = "https://arbiscan.io/address/0x489ee077994B6658eAfA855C308275EAd8097C4A"
	# url = "https://moonbeam.moonscan.io/address/0x4F4495243837681061C4743b74B3eEdf548D56A5?utm_source=immunefi#code"
	url = "https://snowtrace.io/address/0x4d268a7d4C16ceB5a606c173Bd974984343fea13?utm_source=immunefi"
	url = "https://arbiscan.io/address/0x489ee077994B6658eAfA855C308275EAd8097C4A?utm_source=immunefi"
	url = "https://arbiscan.io/address/0x73fe72c9caa0faf0e488570d5898984783e728df?utm_source=immunefi#code"
	
	urls = []
	url = "https://bscscan.com/address/0xC928EF5f74A8B0092f5541c1Cc6b410C2d2410B4?utm_source=immunefi#code"
	urls.append(url)
	url = "https://optimistic.etherscan.io/address/0x4200000000000000000000000000000000000007?utm_source=immunefi"
	urls.append(url)
	url = "https://github.com/fei-protocol/fei-protocol-core/blob/develop/protocol-configuration/mainnetAddresses.ts?utm_source=immunefi"
	urls.append(url)
	base_folder = "./my_project/" # service name

	PR = URLParser()
	PR.parse_all(urls, base_folder)
