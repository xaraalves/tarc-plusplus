#	Atividade Final - Placa numero 09
#
#	Francisco Pegorel Dias, 587702
#	Gabriel Alves Bento, 587869
#	Lizandra Ng, 490040
#
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from twython import Twython
from time import sleep
import datetime
from time import gmtime, strftime
import traceback
import _thread
import facebook

FACEBOOK_APP_ID     = 'THE ID OF YOUR FACEBOOK APP HERE'
FACEBOOK_APP_SECRET = 'THE SECRET OF YOUR FACEBOOK APP HERE'
ACCESS_TOKEN = 'THE FACEBOOK USER ACCESS TOKEN HERE'
FACEBOOK_PROFILE_ID = 'THE ID OF YOUR FACEBOOK PROFILE THAT WILL POST THINGS IN GROUP (AND OWNER OF THE FACEBOOK PAGE)'
GROUP_ID = 'THE ID OF THE FACEBOOK GROUP THE ALERT WILL BE POSTED TO'
PAGE_ACCESS_TOKEN = 'THE TOKEN OF THE FACEBOOK PAGE WHERE ALERTS WILL BE POSTED TO'
PAGE_ID = 'THE ID OF THE PAGE WHERE THE ALERTS WILL BE POSTED TO'
profile = facebook.GraphAPI(access_token=ACCESS_TOKEN, version='2.9')
page = facebook.GraphAPI(access_token=PAGE_ACCESS_TOKEN, version='2.9')

APP_KEY = "THE TWITTER'S APP KEY HERE"
APP_SECRET = "THE TWITTER'S APP SECRET HERE"
OAUTH_TOKEN = "THE TWITTER'S OAUTH TOKEN HERE"
OAUTH_TOKEN_SECRET = "THE TWITTER'S OAUTH TOKEN SECRET HERE"
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def read_Twitter():
	global tweetIdList
	global twitter
	global profile
	global page	
	while True:
		search_results = twitter.search(q='#enchenteSorocaba')
		for tweet in search_results['statuses']:
			sleep(3)
			if tweet['id'] not in tweetIdList and str(tweet['user']['screen_name']) != 'TARCplusplus':
				tweetIdList.append(tweet['id'])
				print ("Tweet do usuario " + str(tweet['user']['screen_name']) + " Data: " + tweet['created_at'] + " Geolocalizacao(long,lat): " + str(tweet['coordinates']))
				print (str(tweet['text']) + "\n")
				page.put_photo(image=open("/twitteralert.png", 'rb'), album_path=PAGE_ID + "/photos", message='Alerta simulativo de enchentes: O usuário do twitter ' + str(tweet['user']['screen_name']) + ', da região de Sorocaba, postou em seu twitter "' + str(tweet['text']) + '". #TARC++')
				#o perfil pega o que foi postado pela pagina e publica no grupo de Catastrofes
				profile.put_photo(image=open("/twitteralert.png", 'rb'), album_path=GROUP_ID + "/photos", message='Alerta simulativo de enchentes: O usuário do twitter ' + str(tweet['user']['screen_name']) + ', da região de Sorocaba, postou em seu twitter "' + str(tweet['text']) + '". #TARC++')
				twitter.update_status(status='Alerta simulativo: Usuário do Twitter ' + str(tweet['user']['screen_name']) + ', na região de Sorocaba, relata enchente! #TARC++ (' + str(datetime.datetime.now().time()) + ')')
		sleep(15)

tweetIdList = []
_thread.start_new_thread(read_Twitter, ())

tiltList = []

def clear_tiltList():
	while True:
		sleep(120)
		del tiltList[:]

def read_tiltList():
	global tiltList
	global twitter
	global profile
	global page
	_thread.start_new_thread(clear_tiltList, ())	
	while True:
		if len(tiltList) >= 5:
			print("Cinco eventos de tremores foram detectados em menos de 20 segundos, enviando notificações!")
			#notificações
			#recebe evento (a fazer) e publica notificação na pagina do facebook
			page.put_photo(image=open("/terremoto.png", 'rb'), album_path=PAGE_ID + "/photos", message='Alerta simulativo: Nossos sensores detectaram risco eminente de um terremoto na região de Sorocaba! #TARCplusplus')
			#o perfil pega o que foi postado pela pagina e publica no grupo de Catastrofes
			profile.put_photo(image=open("/terremoto.png", 'rb'), album_path=GROUP_ID + "/photos", message='Alerta simulativo: Nossos sensores detectaram risco eminente de um terremoto na região de Sorocaba! #TARC++')
			twitter.update_status(status='Alerta simulativo: Nossos sensores detectaram risco eminente de um terremoto na região de Sorocaba! #TARCplusplus ' +  str(datetime.datetime.now().time()))
			sleep(10)

_thread.start_new_thread(read_tiltList, ())

def tiltReceived(client, userdata, message):
	global tiltList
	print("Mensagem recebida no tópico " + message.topic + "e enviada para tratamento.")
	tiltList.append(message.payload)	

temperaturaList = []

def temperaturaReceived(client, userdata, message):
	global temperaturaList
	print("Mensagem recebida no tópico " + message.topic + " e enviada para tratamento.")
	temperaturaList.append((message.payload).decode("utf-8"))

luminosidadeList = []

def luminosidadeReceived(client, userdata, message):
	global luminosidadeList
	print("Mensagem recebida no tópico " + message.topic + " e enviada para tratamento.")
	luminosidadeList.append((message.payload).decode("utf-8"))

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("Server")

myMQTTClient.configureEndpoint("a2c4b1kq2ge0ea.iot.us-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("sub.pem", "sub-private.key", "sub.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()

myMQTTClient.subscribe("tilt", 1, tiltReceived)

def tempestadeAlert():
	global twitter
	global profile
	global page
	#recebe evento (a fazer) e publica notificação na pagina do facebook
	page.put_photo(image=open("/tempestade.jpg", 'rb'), album_path=PAGE_ID + "/photos", message='Alerta simulativo: Nossos sensores detectaram risco eminente de tempestade na região de Sorocaba! Atente-se, as temperaturas aumentaram e a luminosidade diminuiu! #TARCplusplus')
	#o perfil pega o que foi postado pela pagina e publica no grupo de Catastrofes
	profile.put_photo(image=open("/tempestade.jpg", 'rb'), album_path=GROUP_ID + "/photos", message='Alerta simulativo: Nossos sensores detectaram risco eminente de tempestade na região de Sorocaba! Atente-se, as temperaturas aumentaram e a luminosidade diminuiu! #TARCplusplus')
	twitter.update_status(status='Alerta simulativo: Nossos sensores detectaram risco eminente de tempestade na região de Sorocaba! #TARC++' +  str(datetime.datetime.now().time()))
	sleep(30)

def read_sensorsList():
	global temperaturaList
	global luminosidadeList
	while True:
		sleep(10)
		temperaturaList = list(map(float, temperaturaList))
		luminosidadeList = list(map(float, luminosidadeList))
		temperatureChange = (100*(max(temperaturaList) - min(temperaturaList)))/max(temperaturaList)
		temperatureChange = temperatureChange * 10
		luminosidadeChange = (100*(min(luminosidadeList) - max(luminosidadeList)))/max(luminosidadeList)
		print("Realizando leitura das luminosidades e temperaturas recebidas...")
		print("Temperatura alterada em " + str(temperatureChange) + "% e luminosidade em " + str(luminosidadeChange) + "%!")
		if temperatureChange >= 3 and luminosidadeChange <= -10:
			tempestadeAlert()
		del temperaturaList[:]
		del luminosidadeList[:]

myMQTTClient.subscribe("temperatura", 1, temperaturaReceived)
myMQTTClient.subscribe("luminosidade", 1, luminosidadeReceived)

_thread.start_new_thread(read_sensorsList, ())

while True:
	sleep(15)
