import requests, json, os
from dotenv import load_dotenv

load_dotenv()


class ScannerDownloader:
	def __init__(self):
		self.CHAINS = ["ETH", "BSC", "AUR", "POL", "FAN", "ARB", "MOO", "SNO", "OPT"]
		self.URLS = {"ETH": "api.etherscan.io", "AUR": "api.aurorascan.dev", "BSC": "api.bscscan.com", "POL": "api.polygonscan.com", "FAN": "api.ftmscan.com", "ARB": "api.arbiscan.io", "SNO": "api.snowtrace.io", "MOO": "api-moonbeam.moonscan.io", "OPT": "api-optimistic.etherscan.io"}
		self.KEYS = {}
		for chain in self.CHAINS:
			self.KEYS[chain]=(os.getenv(chain + "_APIKEY"))

	def save_file(self, file_name: str, content: str, base_dir: str, is_impl: bool):
		source_path = ""
		if is_impl == True:
			source_path = os.path.abspath(base_dir + "impl_contract/" + file_name)
		else:
			source_path = os.path.abspath(base_dir + file_name)
		os.makedirs(os.path.dirname(source_path), exist_ok=True)
		f = open(source_path, "w")
		f.write(content)


	def split_contract(self, content: str, base_dir: str, is_impl: bool):
		start_idx = -1
		content_len = len(content)
		want = "// File: "
		file_name = ""
		i = 0
		for _ in range(content_len - len(want)):
			if content[i:i+len(want)] == want:
				if start_idx != -1: 
					self.save_file(file_name, content[start_idx:i], base_dir, is_impl)

				j = i+len(want)
				while True:
					if content[j] == '\n':
						file_name = content[i+len(want):j-1]
						break
					j += 1

				start_idx = j + 1

			i += 1

		self.save_file(file_name, content[start_idx:], base_dir, is_impl)


	def downloader(self, chain: str, contract: str, base_dir = "./", is_impl = False):
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
		url = "https://" + self.URLS[chain] + "/api?module=contract&action=getsourcecode&address=" + contract + "&apikey=" + self.KEYS[chain]
		res = requests.get(url, headers=headers)
		res = json.loads(res.content)
		res = res["result"]
		is_proxy = res[0]['Proxy']
		implement = res[0]['Implementation']
		contract_name = res[0]['ContractName']
		source_code = res[0]['SourceCode']

		f = open("json", "w")
		f.write(json.dumps(res[0]))

		if source_code == "": # not verify
			return

		try:
			if source_code[0:2] == "{{":
				source_code = json.loads(source_code[1:-1]) 
				source_code = source_code["sources"]
				for contract in source_code:
					self.save_file(contract, source_code[contract]["content"], base_dir, is_impl)

			else:
				self.save_file(contract_name+".sol", source_code, base_dir, is_impl)

		except:
			self.save_file(contract_name + ".sol", source_code, base_dir, is_impl)
			# split_contract(res, impl)

		if is_proxy == str(1):
			self.downloader(chain, implement, base_dir, True)


if __name__ == '__main__':            
	eth_contract = "0x4Fabb145d64652a948d72533023f6E7A623C7C53"
	bsc_contract ="0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
	poly_contract ="0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
	aurora_contract = "0x0294f2ca320097e098d373d266b21891c3df6a07"
	fantom_contract = "0xe1146b9AC456fCbB60644c36Fd3F868A9072fc6E"
	arb_contract = "0x489ee077994B6658eAfA855C308275EAd8097C4A"
	sno_contract = "0x9e295B5B976a184B14aD8cd72413aD846C299660"
	moo_contract = "0x765277EebeCA2e31912C9946eAe1021199B39C61"
	opt_contract = "0x4200000000000000000000000000000000000007"

	eth_proxy_good_impl_contract = "0xC2b4D7d65797930c4b888C8a639d131a1da07332"
	eth_not_verify_contract = "0xB8B91C47d5a7effD31C4D11D1CB3D4C363A26b4B" # not verfied
	eth_proxy_but_not_verify_contract = "0x289E6c1871f3691e94C1157b965d5aa9093D6328" # proxy is verified but impl is not verfied

	bsc_not_verify_contract = "0x8aaf408e06fEEd6A6a6182EA3c464035748B9B31"
	bsc_proxy_but_not_verify_contract = "0x9984d45674AaE1cb83AB94Ec33c6Ce2CDE91AE81"

	aur_not_verify_contract = "0x4eD2cF27Aa7873d0B8694f295DE7e32A7cd8da83"

	SC = ScannerDownloader()
	SC.downloader("ETH", eth_proxy_good_impl_contract, "./test/") 



# downloader(체인 이름: str, 컨트랙트 주소: str, 베이스 폴더: str)
