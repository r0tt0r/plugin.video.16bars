# -*- coding: utf-8 -*-
#16bars - by r0tt 2012. V0.0.1

import urllib,urllib2,re,string,xbmcaddon,xbmcplugin,xbmcgui,socket,sys,os

if sys.version_info < (2, 7):
    import json as simplejson
else:
    import simplejson

timeout = 25
socket.setdefaulttimeout(timeout)
pluginhandle = int(sys.argv[1])

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
 
cache = StorageServer.StorageServer("ArtworkDownloader",24)

addon = xbmcaddon.Addon('plugin.video.16bars')
scriptpath = addon.getAddonInfo('path')
ACTION_SELECT_ITEM = 7
base='http://www.16bars.de/media/'
logo='/16bars_logo.gif'

def CATEGORIES():
        addDir('Videos International',base + 'video?page=',1,scriptpath + logo)
        addDir('Videos Deutsch',base + 'video-deutsch?page=',1,scriptpath + logo)
        addDir('Videos Classic',base + 'video-classic?page=',1,scriptpath + logo)
        xbmcplugin.endOfDirectory(pluginhandle)
        
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        url=re.sub("page=(.+?)", "page=", url)
        page=re.compile(' &nbsp;<b>(.+?)<\/b>&nbsp; ').findall(link)
        page=str(list(set(page)))
        page=int(str(page).strip("'[]'")) + 1
        pageurl=url + str(page)
        addDir("Go To Page "+str(page), pageurl, 1, "")
        title=re.compile('    (.+?)<span style="font-weight: normal;">(.+?)</span> </a></h4>').findall(link)
        video1=re.compile('    <a href=\"(\/media\/.+?)\"><img src=\"').findall(link)
        video=['http://www.16bars.de'+li for li in video1]
        thumb=re.compile('\"><img src=\"(.+?)\" alt=').findall(link)
        match=zip(title, video, thumb)
        for name,url,thumb in match:
            name = str(name).replace('"','').replace(',','').replace('(','').replace(')','').replace("'","").replace('\\xc3\\xb6','ö').replace('\\xc3\\xbc','ü').replace('\\xc3\\xa4','ä').replace('\\xfc','ü').replace('\\xf6','ö')
            addDir(name,url,2,thumb)
        xbmcplugin.endOfDirectory(pluginhandle)      

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('/embed/(.+?)\"').findall(link)
        for url in match:
            Vid = str(match).strip("['']")
            url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s' % Vid
            addLink(name,url,'')
        xbmcplugin.endOfDirectory(pluginhandle)

def playVid(Vid):
        action=''
        if action == ACTION_SELECT_ITEM:
            url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s' % Vid
            xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
        xbmcplugin.endOfDirectory(pluginhandle)
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable','true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
                  
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
