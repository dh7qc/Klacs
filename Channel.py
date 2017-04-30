import json 
import socket 
import threading 

		
class Channel:   
	MAX_ARCHIVE = 50
	messages_archived = 0
	def __init__(self, server, channel_id, users=None):
		self.server = server
		# self.name = name
		self.id = channel_id
		self.users = {} if users is None else users
		self.archive = []
		# Note about the archive: List of dictionaries that get sent to the client??
		self.admins = []
		self.m_password = ''  # channel password, empty if public channel

	def postMessage(self, username, data):
		temp = data['data']
		msg = temp['message']
		time = temp['date/time']
		self.storeMessage(username, msg, time)



	def assignAdmin(self, username):
		self.admins.append(username)


	def revokeAdmin(self, username):
		self.admins.remove(username)


	def storeMessage(self, username, message, timestamp):
		if len(self.archive) < self.MAX_ARCHIVE:
			self.archive.append({'username':username, 'message':message, 'timestamp':timestamp})
		else:
			pass


	def distributeMessageArchive(self):
		for message in self.archive:
			pass
			# send each message to server
			# the past 50 messages in the channel json, show to each user
			# append message to archive,delete one on top


	def addUser(self, data):
		if (self.users[data['data']['targetUser']] == -1 and self.users[data['username']] < 1):  # Only admins and higher can readd a banned user
			print("Error: Banned user")
		elif (self.m_password != '' and self.users[data['username']] < 1):  # Only admins and higher can add command a user to private servers
			print("Error: private server")
		elif (self.users[data['data']['targetUser']] > -1):  # cannot add user already in channel
			print("Error: User already in channel")
		else:  # set target_user to normal status
			self.users[data['data']['targetUser']] = 1


	def banUser(self, data):
		if (self.users[data['username']] > 0 and self.users[data['username']] > self.users[data['data']['targetUser']]):
			self.users[data['data']['targetUser']] = -1
		else:
			print("Error: User permission level too low")
