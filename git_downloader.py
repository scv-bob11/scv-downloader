import git
import os
import sys
from urllib.parse import urljoin, urlparse

class Test:
	def __init__(self):
		return

	def get_files_in_dir(self, root_dir, result = []):
		files = os.listdir(root_dir)
		for file in files:
			path = os.path.join(root_dir, file)
			result.append(path)
			if os.path.isdir(path):
				self.get_files_in_dir(path, result)
		return result

class GitDownloader:
	def __init__(self):
		self.test = Test()
		return

	def is_github(self, url):
		parts = urlparse(url)
		if parts.netloc == "github.com":
			return True
		return False

	def is_gitlab(self, url):
		None

	def get_git_url(self, url):
		if self.is_github(url) == False:
			return ""
		parts = urlparse(url)
		paths = parts.path.split("/")
		git_url = "https://" + parts.netloc
		for i in range(3):
			git_url += paths[i] + "/"
		print(git_url)
		return git_url

	def make_safe_dir(self, base_dir):
		if not os.path.exists(base_dir):
			os.makedirs(base_dir)

	def git_clone(self, base_dir, git_url):
		self.make_safe_dir(base_dir)
		git.Git(base_dir).clone(git_url)

	# 확장자가 .sol이 아니면 전부 지움.
	def clear_etc(self, base_dir): 
		file_list = self.test.get_files_in_dir(base_dir)
		file_list.sort(reverse=True)
		for f in file_list:
			extension = os.path.splitext(f)[1]
			try:
				if "" == extension:
					if os.path.isfile(f):
						os.remove(f)
					else:
						os.rmdir(f)
				elif ".sol" != extension:
					os.remove(f)
			except:
				continue
		return


	def download(self, base_dir, url):
		git_url = self.get_git_url(url)
		if git_url == "":
			return
		self.git_clone(base_dir, git_url)
		# self.clear_etc(base_dir)

if __name__ == '__main__':
	urls = "https://github.com/fei-protocol/fei-protocol-core/blob/develop/protocol-configuration/mainnetAddresses.ts?utm_source=immunefi"
	GitDownloader().download("./", urls)
