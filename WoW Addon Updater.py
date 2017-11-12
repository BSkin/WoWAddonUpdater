import urllib.request
import re
import zipfile
import configparser
import os
import shutil

def getAddonDownloadLink(url):
	downloadRegex = '<a class="download__link" href="(.*)">here</a>'
	response = urllib.request.urlopen(url + '/download').read().decode('utf-8')
	return re.search(downloadRegex, response).group(1)

def getAddonUpdateDataEpoch(url):
	updateRegex = 'Last Updated:.*data-epoch="([0-9]*)"'
	response = urllib.request.urlopen(url).read().decode('utf-8')
	return re.search(updateRegex, response).group(1)
	
def addonUpToDate(config, key, value):
	if (not 'INSTALLED' in config):
		return False
	installed = config['INSTALLED']
	
	if (not key in installed):
		return False
		
	return installed[key] == value

def updateAddonFiles(url):
	if (os.path.exists('temp')):
		shutil.rmtree('temp')
	os.makedirs('temp')

	downloadPath = getAddonDownloadLink(url)
	urllib.request.urlretrieve ('https://curseforge.com/' + downloadPath, "addon.zip")
	with zipfile.ZipFile("addon.zip","r") as zip_ref:
		zip_ref.extractall("temp")
		
	for item in os.listdir('temp'):
		if (os.path.exists(addonLocation + '\\' + item)):
			shutil.rmtree(addonLocation + '\\' + item)
		shutil.move('temp' + '\\' + item, addonLocation)
		
	if os.path.exists('addon.zip'):
		os.remove('addon.zip')
		
	if (os.path.exists('temp')):
		shutil.rmtree('temp')
	
def updateAddon(config, url):
	key = url.replace('https://', '')

	latestUpdate = getAddonUpdateDataEpoch(url)
	if addonUpToDate(config, key, latestUpdate):
		if (showIgnored):
			print('up to date: ' + key)
		return
		
	updateAddonFiles(url)
	print('updated {}'.format(url))
	
	if not 'INSTALLED' in config:
		config['INSTALLED'] = {key: latestUpdate}
	else:
		config['INSTALLED'][key] = latestUpdate
		
	with open(installedFile, 'w') as configfile:
		config.write(configfile, space_around_delimiters=False)

installedFile = 'installed.cfg'
addonLocation = 'C:\Program Files (x86)\World of Warcraft\Interface\AddOns'
showIgnored = True

config = configparser.ConfigParser()
config.read(installedFile)

with open('addons.txt') as file:
	lines = file.read().splitlines()
	for line in lines:
		try:
			updateAddon(config, line)
		except Exception as e:
			print('Error updating {}: {}'.format(line, e))

	







