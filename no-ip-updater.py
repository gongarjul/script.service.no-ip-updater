import urllib2
import httplib
import xbmcgui
import xbmcaddon
import time
from datetime import datetime, timedelta
import base64

addon =xbmcaddon.Addon (id='script.service.no-ip-updater')

hostname = addon.getSetting('hostname')
username = addon.getSetting('username')
password = addon.getSetting('password')


urlUsedToUpdate = 'http://dynupdate.no-ip.com/nic/update'
secondsToUpdate = 5*60
td = timedelta(seconds = secondsToUpdate + 1)

if len(hostname) == 0 or len(username) == 0 or len(password) == 0:
    print('-- script.service.no-ip-updater --')
    print('Some settings are empty, review the configuration and restart the addon or xbmc')
    xbmcgui.Dialog().ok('no-ip updater', 'Some settings are empty, please:', '\t-Review the configuration', '\t-Restart the addon or xbmc')

else:

    print('-- script.service.no-ip-updater --')
    print('Config data read')

    while True:
        
        if td.seconds > secondsToUpdate:
        
            try:
                print('-- script.service.no-ip-updater --')
                print('Requesting no-ip for updates')
                req = urllib2.Request('%s?hostname=%s' % (urlUsedToUpdate, hostname)) 
                req.add_header('User-Agent', 'GGJs update service for xbmc/0.2  gongarjul@gmail.com') 
                base64string = base64.encodestring('%s:%s' % (username, password))
                req.add_header("Authorization", "Basic %s" % base64string)            
                f = urllib2.urlopen(req)
                
            except urllib2.URLError as e:
                print('Error requesting no-ip for updates, reason: %s' % e.reason)
                xbmcgui.Dialog().ok('no-ip updater', 'Error requesting no-ip for updates, reason: %s' % e.reason)
                break
                
            else:
                #the request is well formed
                lastUpdate = datetime.now()
                response = str(f.read())
                if response.find('good') >= 0:
                    print('DNS hostname update successful')
                    print('%s IP is: %s' % (hostname,response.split(' ')[1]))
                    secondsToUpdate = 5*60
                elif response.find('nochg') >= 0:
                    print('IP address is current, no update performed')
                    print('%s IP is: %s' % (hostname,response.split(' ')[1]))
                    secondsToUpdate = 5*60
                elif response.find('nohost') >= 0:
                    print('Hostname supplied does not exist under specified account')
                    print('Review the hostname configuration and restart the addon or xbmc')
                    xbmcgui.Dialog().ok('no-ip updater', 'Hostname supplied does not exist, please:', '\t-Review the hostname configuration', '\t-Restart the addon or xbmc')
                    break
                elif response.find('badauth') >= 0:
                    print('Invalid username password combination')
                    print('Review the username/password configuration and restart the addon or xbmc')                
                    xbmcgui.Dialog().ok('no-ip updater', 'Invalid username password combination, please:', '\t-Review the username/password configuration', '\t-Restart the addon or xbmc')
                    break
                elif response.find('badagent') >= 0:
                    print('Client disabled')
                    print('Send an e-mail to gongarjul@gmail.com')
                    xbmcgui.Dialog().ok('no-ip updater', 'Client disabled, please:', '\t-Send an e-mail to gongarjul@gmail.com')
                    break
                elif response.find('!donator') >= 0:
                    print('An update request was sent including a feature')
                    print('that is not available to that particular user')
                    print('Send an e-mail to gongarjul@gmail.com')
                    xbmcgui.Dialog().ok('no-ip updater', 'An update request was sent including a feature\nthat is not available to that particular user', '\t-Send an e-mail to gongarjul@gmail.com')
                    break
                elif response.find('abuse') >= 0:
                    print('Username is blocked due to abuse')
                    xbmcgui.Dialog().ok('no-ip updater', 'Username is blocked due to abuse')
                    break
                elif response.find('911') >= 0:
                    print('Fatal error on no-ip')
                    print('Next try to update will be on 30 minutes')
                    xbmcgui.Dialog().ok('no-ip updater', 'Fatal error on no-ip', 'Next try to update will be on 30 minutes')
                    secondsToUpdate = 30*60
                else:
                    print('Unknown result code:' + response)
                    print('Send an e-mail to gongarjul@gmail.com')
                    xbmcgui.Dialog().ok('no-ip updater', 'Unknown result code:' + response, 'Send an e-mail to gongarjul@gmail.com')
                    break
        
        td = datetime.now() - lastUpdate    
        
        if xbmc.abortRequested:
            break
