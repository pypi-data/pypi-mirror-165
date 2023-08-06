from typing import Any
import requests
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import base64
import json
from datetime import datetime, timedelta

class tokenGenerator():
	# account example - py_signature_parser@dozi-stg-ds-apps-1.iam.gserviceaccount.com
	# audience example - 1042519062771-rghbs1ied8kno7l00mlnko5r7sgjea2o.apps.googleusercontent.com
	# get from https://console.cloud.google.com/apis/credentials?project=dozi-stg-ds-apps-1
	# audience - OAuth 2.0 Client IDs, Client ID
	# account - one of the service accounts listed
	tokens = {}
	def __init__(self, conf):
		self.conf = conf
		for key in conf:
			self.tokens[key] = ''

	def generateToken(self, type):
		if self.isExpired(type):
			self.resetToken(type)
		if not type or not self.conf[type]:
			return ''
		conf: Any = self.conf[type]
		if not conf['account']:
			print('please specify account')
			return ''
		if not conf['target_audience']:
			print('please specify target audience')
			return ''
		if not self.tokens[type]:
			credentials = self.authorize()
			token = self.getToken(credentials, conf)
			if self.conf[type]['iap']:
				token = self.buildIdToken(credentials, token, conf)
			self.tokens[type] = token

		return self.tokens[type]

	def authorize(self):
		# return google.auth.default(
		# 	scopes=['https://www.googleapis.com/auth/cloud-platform'])
		return GoogleCredentials.get_application_default()

	def getToken(self, credentials, conf):
		client_id = credentials.client_id
		client_secret = credentials.client_secret
		aud = credentials.token_uri
		iat = int(datetime.now().timestamp())
		one_hours_from_now = datetime.now() + timedelta(hours=1)
		exp = int(one_hours_from_now.timestamp())
		service = discovery.build('iam', 'v1', credentials=credentials)

		name = f'projects/{conf["host"]}/serviceAccounts/{conf["account"]}'
		data ={
			'url': f'https://iam.googleapis.com/v1/projects/-/serviceAccounts/{conf["account"]}:signJwt',
			'data': {
				'payload': json.dumps({"aud": aud,"target_audience": conf["target_audience"],"sub": conf["account"],"iss": conf["account"],"iat": iat, "exp": exp})
			}
		}
		request = service.projects().serviceAccounts().signJwt(name=name, body={'payload': data["data"]["payload"]})
		response = request.execute()
		return response['signedJwt']


	def buildIdToken(self, client, jwtToken, conf):
		try:
			data = {
				"method": 'post',
				"url": 'https://www.googleapis.com/oauth2/v4/token',
				"data": {
    				'grant_type': "urn:ietf:params:oauth:grant-type:jwt-bearer",
    				'assertion': jwtToken
                }
			}
			# print('data', data)
			result = requests.post(data['url'], data['data'])
			if result and result.content:
				parsed = json.loads(result.content)
				print("[refreshTokens] token for host " + conf['host'] + " refreshed successfully")
				return parsed['id_token']
			else:
				print('no data.id_token returned from googleapis:signJwt')
		except Exception as ex:
			print("[refreshTokens] token for host " + conf['host'] + " failed to refresh")
			print(ex)

	def isExpired(self, type):
		isExpired = True
		if self.tokens[type]:
			decoded = self.parse_id_token(self.tokens[type])
			if decoded and int(decoded['exp']) > int(datetime.now().timestamp()):
				isExpired = False
		return isExpired

	def isExpiredToken(self, token):
		isExpired = True
		decoded = self.parse_id_token(token)
		if decoded and int(decoded['exp']) > int(datetime.now().timestamp()):
			isExpired = False
		return isExpired

	def resetToken(self, type):
		self.tokens[type] = ''

	@staticmethod
	def parse_id_token(token: str) -> dict:
		"""
		Parse Google OAuth2.0 id_token payload
		An ID token has the following structure: Base64(JOSE header).Base64(Payload).Base64(Signature)
		"""
		parts = token.split(".")
		if len(parts) != 3:
			raise Exception("Incorrect id token format")
		payload = parts[1]
		padded = payload + "=" * (4 - len(payload) % 4)
		decoded = base64.b64decode(padded)
		return json.loads(decoded)

if __name__ == '__main__':
	conf = {
		"STG_Conf": {
			"account": '{your service account}',  # need to get from dev ops
			"host": '{your project id}',
			"target_audience": '{your client id}',
			"iap": True,
		},
		"PRD_Conf": {
			"account": '{your service account}',  # need to get from dev ops
			"host": '{your project id}',
			"target_audience": '{your client id}',
			"iap": True,
		}
	}
	instance = tokenGenerator(conf)
	token = instance.generateToken('STG_Conf')
	print('token', token)

