import hashlib
import base64
import pycurl
import os
#hate such imports but i had no choice
from StringIO import *

#javascript:document.write(document.cookie) - for RemixId

class GUploader:
    def __init__(self, userID, myID, myEMail, myPassword, myRemixId, graffitiFile):
        self.userID = userID
        self.myID = myID
        self.myEMail = myEMail
        self.myPassword = hashlib.md5(myPassword).hexdigest()
        self.myRemixId = myRemixId
        self.graffitiFile = os.path.abspath(graffitiFile);
        self.curl = pycurl.Curl()
        self.st = StringIO()
    
    def __del__(self):
        self.curl.close()
    
    def pngsigMD5(self):
        pngsize = os.path.getsize(self.graffitiFile)
        pngcontent = open(self.graffitiFile, 'rb').read(pngsize)
        pngsigB64 = base64.b64encode(pngcontent)[0:1024]
        return hashlib.md5(pngsigB64).hexdigest()
    
    def makeCookie(self):
        return 'remixlang=0; remixchk=5; remixautobookmark=14; remixmid=' + self.myID + '; remixemail=' + self.myEMail + '; remixpass=' + self.myPassword + '; remixsid=' + self.myRemixId + ';'          
      
    def config(self):
        def setoptArray(curlObj, optArray):
            for optName, optValue in optArray.iteritems():
                opt = getattr(pycurl, optName)
                curlObj.setopt(opt, optValue)
        options = {
        "URL" : 'http://vkontakte.ru/graffiti.php?to_id=' + self.userID + '&group_id=0',
        "WRITEFUNCTION" : self.st.write, 
        "HTTPPOST" : [
            ('Signature', self.pngsigMD5()),
            ('Filedata', (pycurl.FORM_FILE, self.graffitiFile)),
            ('Upload','Submit Query')
        ],
        "REFERER" : 'http://vkontakte.ru/swf/Graffiti.swf?15',
        "USERAGENT" : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8 (.NET CLR 3.5.30729) FirePHP/0.2.4',
        "COOKIE" : self.makeCookie(),
        "HTTPHEADER" : [
            'Host: vkontakte.ru',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: ru,en-us;q=0.7,en;q=0.3',
            'Accept-Encoding: gzip,deflate',
            'Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive: 300',
            'Connection: keep-alive',  
        ],
        }
        setoptArray(self.curl, options)

    def execute(self):
        self.curl.perform()
        
    def GetValue(self):
        return self.st.getvalue()

upl = GUploader(
	'', #User ID 
	'', #My Id
	'', #My e-mail
	'*******', #mypass
 	'113f7b7215724745ab63076b5547c07eff1ce51da370a26f6f2931f8', 
	'graffiti.png')

upl.config()
upl.execute()
