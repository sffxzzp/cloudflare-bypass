# -*- coding: UTF-8 -*-
import re, requests
from urllib.parse import quote as urlencode

def findstr(rule, string):
	find_str = re.compile(rule)
	return find_str.findall(string)

class weblib:
	def __init__(self):
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
		}
		self.jar = requests.cookies.RequestsCookieJar()
	def setCookie(self, key, value):
		self.jar.set(key, value)
	def getCookie(self):
		return requests.utils.dict_from_cookiejar(self.cookies)
	def get(self, url, chardet=False):
		try:
			req = requests.get(url, headers = self.headers, cookies = self.jar, timeout=90)
			self.cookies = req.cookies
			if chardet:
				req.encoding = requests.utils.get_encodings_from_content(req.text)[0]
			return req.text
		except:
			return ''
	def post(self, url, postdata, chardet=False):
		try:
			req = requests.post(url, headers = self.headers, cookies = self.jar, data = postdata, timeout=90)
			self.cookies = req.cookies
			if chardet:
				req.encoding = requests.utils.get_encodings_from_content(req.text)[0]
			return req.text
		except:
			return ''

class cloudflare:
	def __init__(self, url):
		self.weblib = weblib()
		self.get(url)
	def get(self, url):
		html = self.weblib.get(url)
		if 'cf-browser-verification' in html or 'complete_sec_check' in html:
			urlSch = 'https://' if 'https://' in url else 'http://'
			urlBase = url.replace('http://', '').replace('https://', '').split('/')[0]
			urlLen = len(urlBase)
			vName = findstr('s,t,o,p,b,r,e,a,k,i,n,g,f, (.*)=\{"(.*)":(.*)};', html)[0]
			fName, sName, fCode = vName;
			fCode = self.decodeJSCode(fCode);
			sCode = findstr(';.*121\'', html)[0].split(';')[1:-3]
			for code in sCode:
				pre, code = code.replace(fName+'.'+sName, '').split('=')
				fCode = eval('fCode'+pre+str(self.decodeJSCode(code)))
			postPath = urlSch + urlBase + findstr('form id="challenge-form" action="(.*?)"', html)[0]
			s = urlencode(findstr('input type="hidden" name="s" value="(.*?)"', html)[0], safe='')
			jschl_vc = findstr('input type="hidden" name="jschl_vc" value="(.*?)"', html)[0]
			passkey = findstr('input type="hidden" name="pass" value="(.*?)"', html)[0]
			answer = round(fCode+urlLen, 10);
			postURL = postPath+'?s='+s+'&jschl_vc='+jschl_vc+'&pass='+passkey+'&jschl_answer='+str(answer)
			result = self.weblib.get(postURL)
			return result
		return html
	def decodeJSCode(self, code):
		code = code.replace('!![]', '1').replace('!+[]', '1').replace('(+[])', '(0)').replace('+((', '(').replace('))', ')').split('/')
		fnumu = ""
		fnumd = ""
		for num in findstr('\(.*?\)', code[0].replace('+[]', '')):
			fnumu += str(eval(num))
		for num in findstr('\(.*?\)', code[1].replace('+[]', '')):
			fnumd += str(eval(num))
		return int(fnumu)/int(fnumd)

web = cloudflare('https://steamdb.info/')
content = web.get('https://steamdb.info/sub/344127/')
print(web.weblib.getCookie())
print(content)
