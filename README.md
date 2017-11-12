# WoWAddonUpdater
Updates WoW Addons

1. Add addons.txt in the same path as WoW Addon Updater.py
    addons.txt should contain a list of curse links, eg
        https://www.curseforge.com/wow/addons/bagnon
        https://www.curseforge.com/wow/addons/bartender4
        https://www.curseforge.com/wow/addons/big-wigs
        
2. Run WoW Addon Updater.py
    installed.cfg is used to keep track of which version has been installed. If you delete or modify this file the script will either reinstall the current version or not update the addon at all.
