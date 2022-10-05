from asyncio import subprocess
import git
import os
import sys
from urllib.parse import urljoin, urlparse

import subprocess

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
	github_list = []

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
		git_url = "https://g:s@" + parts.netloc # username:password@ add
		if len(paths) < 3: # repo를 제시 안한경우
			return ""
		for i in range(3):
			git_url += paths[i] + "/"
		print(git_url)
		return git_url

	def make_safe_dir(self, base_dir):
		if not os.path.exists(base_dir):
			os.makedirs(base_dir)

	def git_clone(self, base_dir, git_url):
		self.make_safe_dir(base_dir)
		try:
			git.Git(base_dir).clone(git_url) # 이미 git repo가 존재하는 경우는 pass
		except git.exc.GitCommandError as err:
			if "already exists and is not an empty directory" in str(err):
				return
			if "Authentication failed" in str(err):
				return
			else:
				print(err)
				exit(-1) 

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
		# if package.json exists, cd proejct; npm install

		git_dir = git_url.split("/")
		GitDownloader.github_list.append(base_dir + git_dir[-2])

		# cmd = "cd " + base_dir + git_dir[-2] + "; sudo npm install --save --legacy-peer-deps --no-audit"
		
		# dir_list = os.listdir(base_dir + git_dir[-2])
		# if "package.json" in dir_list:
		# 	subprocess.Popen(cmd, shell=True) # 
		# 	print("npm install")
		# return
		
		# subprocess.call(cmd, shell=True)
		
		# self.clear_etc(base_dir)
	def get_github_file_dir(self):
		f = open("github_list", "w")
		GitDownloader.github_list = set(GitDownloader.github_list)
		for g in GitDownloader.github_list:
			f.write(g+"\n")

if __name__ == '__main__':
	urls = "https://github.com/fei-protocol/fei-protocol-core"
	GitDownloader().download("./", urls)
