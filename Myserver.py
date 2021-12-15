from socket import *
import sys
from time import *
import os
import mimetypes
import base64
from glob import *
from threading import *
import threading
import logging
import random
from config import *
import uuid

class decoder():
	def __init__(self,recvData):
		self.UserAgent = None
		self.host = None
		self.method_type = None
		self.filename = None
		self.http_version = None
		self.Content_Length = None
		self.Accept_Encoding  = None
		self.server = 'Apache/2.4.41(ubuntu)'
		self.data = None
		self.decode_header(recvData)
		self.cookie = None

	def decode_header(self,recvData):
		try:
			data = recvData.decode()
			data,body = data.split("\r\n\r\n")
		except UnicodeDecodeError:
			new_data = recvData.split(b"\r\n\r\n")
			data = new_data[0].decode()
			body = new_data[1]

		header_list = dict()
		info = data.split('\r\n')
		self.method_type = info[0].split(' ')[0]
		self.filename = info[0].split(' ')[1].replace('/','',1)
		self.http_version = info[0].split(' ')[2]
		for i in info[1:]:
			h1,h2 = i.split(": ")
			header_list[h1] = h2

		if 'Content-Length: ' in data:
			self.Content_Length = header_list['Content-Length']
		else:
			self.Content_Length = 0

		if 'Accept-Encoding: ' in data:
			self.Accept_Encoding = header_list['Accept-Encoding']
		else:
			self.Accept_Encoding = '-'
		if 'User-Agent: 'in data:
			self.UserAgent = header_list['User-Agent']

		if 'Host: 'in data:
			self.host = header_list['Host']
		self.data = body
		
		if 'Cookie: ' in data:
			self.cookie = header_list['Cookie']

def fileLength(file_name):
    l = str(os.path.getsize(file_name))
    return l

def curr_time():
	t = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
	return t

def Last_Modified(file_name):
	last = os.path.getmtime(file_name)
	x = ctime(last)
	y = x.split()
	time = y[0] + ", " + y[2] + " " + y[1] + " " + y[4] + " " + y[3] + " GMT"
	return time

def Location(file_name):
    p = os.path.abspath(file_name)
    return p

def type(file_name):
    t,file_encoding = mimetypes.guess_type(file_name)
    return t

def cookies():
    cookie_no = str(uuid.uuid1())
    with open ("cookie_file.txt", "a+") as file:
        file.write(cookie_no + "\n")

    return cookie_no

def headers(filename,status,obj):
	hdr = "HTTP/1.1 "+status+"\n"
	hdr += "Date: "+curr_time()+"\n"
	hdr += "Last-Modified: "+Last_Modified(filename)+"\n"
	hdr += "Server: Apache/2.4.41(ubuntu)\n"
	hdr += "Host: " + str("127.0.0.1") + ":" + str(PortNo) + "\n"
	hdr += "Accept: */*\n"
	hdr += "User-Agent: "+obj.UserAgent+"\n"
	hdr += "Accept-Encoding: "+obj.Accept_Encoding+"\n"
	hdr += "Content-Length: "+ fileLength(filename)+"\n"
	hdr += "Content-Location: "+Location(filename)+"\n"
	hdr += "Content-Type: "+type(filename)+"\n"
	if (obj.cookie == None):
		hdr += "Set-Cookie: id=" + cookies() + " Max-Age=60\r\n"

	hdr += "Accept-Ranges: bytes\n"
	hdr += "Range: bytes=0-\n"
	hdr += "Accept-Charset: utf-8\n"
	hdr += "Connection: Keep-Alive\n\n"
	return hdr

def Writing_format(filename,data):
	if(filename.endswith(".txt") or filename.endswith(".html") or filename.endswith(".csv")):
		file = open(filename,'w')
		file.write(data)
		file.close()
	else:
		with open(filename,'wb') as otherformat:
			otherformat.write(data)
			otherformat.close()
	return

def Reading_format(filename):
	if(filename.endswith(".txt") or filename.endswith(".html") or filename.endswith(".csv")):
		file = open(filename,'r')
		final = file.read().encode()
		file.close()
		return final
	else:
		with open(filename,'rb') as otherformat:
			final = otherformat.read()
			otherformat.close()
			return final

def post_rename(filename):
	name,extension = filename.split(".")
	x = set(glob(name + "*"))
	y = set(glob("*." + extension))
	if(x & y):
		files = (x & y)
	i = len(files)
	new = name + "(" +str(i) + ")" + "." +extension
	return new

def Authentication(Recieve):
	Recieve = Recieve.decode()
	new = Recieve.split("Basic ")[1].split("\r\n")[0]
	fetch = base64.decodebytes(new.encode()).decode()
	username = fetch.split(':')[0]
	password = fetch.split(':')[1]
	if(username == USERNAME and password == PASSWORD):
		return True
	return False
	
def logging_levels(level):
    if(level == 'level1'):
        logging.basicConfig(filename = "user.log", format = '[%(asctime)s]: %(message)s', level = logging.INFO)
    elif(level == 'level2'):
        logging.basicConfig(filename = "debug.log", format = '[%(asctime)s]: %(message)s', level = logging.DEBUG)
    elif(level == 'level3'):
        logging.basicConfig(filename = "developer.log", format = '[%(asctime)s]: %(message)s', level = logging.WARNING)
    else:
        print("logging level is not valid")
        sys.exit(0)		

def all_methods(Recieve):
	obj = decoder(Recieve)
	URI = "/"+obj.filename
	
	if obj.http_version not in Http_versions:
		status = '505'
		versions = "HTTP/1.1 "+status+"\n"
		versions += "Date: "+curr_time()+"\n"
		versions += "Server: Apache/2.4.41(ubuntu)\n"
		versions += "Content-Length: "+fileLength("505_version.html") +"\n"
		versions += "Connection: close\n"
		versions += "Content-Type: text/html\n\n"
		file = open("505_version.html", "r")
		file_info = file.read()
		file.close()
		final_output = versions + file_info
		connectionSocket.send(final_output.encode())
		logging.debug(f"{ip}:{PortNo} \"{obj.http_version}  Version is not supported.")
		logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent}")
		logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
		return
	elif (mimetypes.guess_type(obj.filename)[0] not  in media):
		status = '415'
		unsupported = "HTTP/1.1 "+status+"\n"
		unsupported += "Date: "+curr_time()+"\n"
		unsupported += "Server: Apache/2.4.41(ubuntu)\n"
		unsupported += "Content-Length: "+fileLength("415_Unsupported.html") +"\n"
		unsupported += "Connection: close\n"
		unsupported += "Content-Type: text/html\n\n"
		file = open("415_Unsupported.html", "r")
		file_info = file.read()
		file.close()
		final_output = unsupported + file_info
		connectionSocket.send(final_output.encode())
		logging.debug(f"{ip}:{PortNo} \"{obj.filename} This File format is not supported ")
		logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent}")
		logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
		return
	elif(len(URI) > MAX_LENGTH):
		status = '414'
		max_uri = "HTTP/1.1 "+status+"\n"
		max_uri += "Date: "+curr_time()+"\n"
		max_uri += "Server: Apache/2.4.41(ubuntu)\n"
		max_uri += "Content-Length: "+fileLength("414_URI_tooLong.html") +"\n"
		max_uri += "Connection: close\n"
		max_uri += "Content-Type: text/html\n\n"
		file = open("414_URI_tooLong.html", "r")
		file_info = file.read()
		file.close()
		final_output = max_uri + file_info
		connectionSocket.send(final_output.encode())
		logging.debug(f"{ip}:{PortNo} \"{obj.filename} {MAX_LENGTH} URI too long ")
		logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent}")
		logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
		return
	elif obj.method_type in Allow:
		if obj.method_type == 'GET':
			if (os.path.isfile(obj.filename)):
				if(os.access(obj.filename, os.R_OK) and os.access(obj.filename, os.W_OK)):
					status = '200'
					final_output = headers(obj.filename,status,obj)
					connectionSocket.send(final_output.encode())
					connectionSocket.send(Reading_format(obj.filename))
					# connectionSocket.close()
					logging.debug(f"{ip}:{PortNo} \"{obj.filename} Accessed Successfully.")
					logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
					logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
					return
				else:
					status = '403'
					forbidden = "HTTP/1.1 "+status+"\n"
					forbidden += "Date: "+curr_time()+"\n"
					forbidden += "Server: Apache/2.4.41(ubuntu)\n"
					forbidden += "Content-Length: "+fileLength("403_Forbidden.html") +"\n"
					forbidden += "Connection: close\n"
					forbidden += "Content-Type: text/html\n\n"
					file = open('403_Forbidden.html','r')
					file_info = file.read()
					file.close()
					final_output = forbidden + file_info
					connectionSocket.send(final_output.encode())
					logging.debug(f"{ip}:{PortNo} \"Requested File {obj.filename} was Forbidden")
					logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
					logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
					return
			else:
				status = '404'
				not_found = "HTTP/1.1 "+status+"\n"
				not_found += "Date: "+curr_time()+"\n"
				not_found += "Server: Apache/2.4.41(ubuntu)\n"
				not_found += "Host: " + str("127.0.0.1") + ":" + str(PortNo) + "\n"
				not_found += "Content-Length: "+ fileLength('404_NotFound.html')+"\n"
				not_found += "Content-Location: "+Location('404_NotFound.html')+"\n"
				not_found += "Content-Type: "+type('404_NotFound.html')+"\n\n"
				file = open('404_NotFound.html','r')
				file_info = file.read()
				file.close()
				final_output = not_found + file_info
				connectionSocket.send(final_output.encode())
				logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
				logging.debug(f"{ip}:{PortNo} \"{obj.filename} File Not Found ")
				logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
				return
		elif obj.method_type == 'HEAD':
			if (os.path.isfile(obj.filename)):
				if(os.access(obj.filename, os.R_OK) and os.access(obj.filename, os.W_OK)):
					status = '200'
					final_output = headers(obj.filename,status,obj)
					connectionSocket.send(final_output.encode())
					logging.debug(f"{ip}:{PortNo} \"{obj.filename} Head Successful.")
					logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
					logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
					return
				else:
					status = '403'
					forbidden = "HTTP/1.1 "+status+"\n"
					forbidden += "Date: "+curr_time()+"\n"
					forbidden += "Server: Apache/2.4.41(ubuntu)\n"
					forbidden += "Content-Length: "+fileLength("403_Forbidden.html") +"\n"
					forbidden += "Connection: close\n"
					forbidden += "Content-Type: text/html\n\n"
					final_output = forbidden
					connectionSocket.send(final_output.encode())
					logging.debug(f"{ip}:{PortNo} \"Requested File {obj.filename} was Forbidden")
					logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
					logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
					return
			else:
				status = '404'
				not_found = "HTTP/1.1 "+status+"\n"
				not_found += "Date: "+curr_time()+"\n"
				not_found += "Server: Apache/2.4.41(ubuntu)\n"
				not_found += "Host: " + str("127.0.0.1") + ":" + str(PortNo) + "\n"
				not_found += "Content-Length: "+ fileLength('404_NotFound.html')+"\n"
				not_found += "Content-Location: "+Location('404_NotFound.html')+"\n"
				not_found += "Content-Type: "+type('404_NotFound.html')+"\n\n"
				final_output = not_found
				connectionSocket.send(final_output.encode())
				logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
				logging.debug(f"{ip}:{PortNo} \"{obj.filename} File Not Found ")
				logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
				return
		elif obj.method_type == 'DELETE':
			if (os.path.isfile(obj.filename)):
				if(os.access(obj.filename, os.R_OK) and os.access(obj.filename, os.W_OK)):
					if Authentication(Recieve):
						status = '200'
						final_output = headers(obj.filename,status,obj)
						os.remove(obj.filename)
						connectionSocket.send(final_output.encode())
						logging.debug(f"{ip}:{PortNo} \"{obj.filename} File Deleted Successfully. ")
						logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
						logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
					else:
						status = '401'
						data = "HTTP/1.1 401 Unauthorised\n"
						data += "Date: "+curr_time()+"\n"
						data += "Server: Apache/2.4.41(ubuntu)\n"
						data += "Last-Modified: "+Last_Modified(obj.filename)+"\n"
						data += "Content-Length: "+ fileLength('401_Unauthorized.html')+"\n"
						data += "Connection: close\n"
						data += "Content-Type: text/html\n\n"
						file = open('401_Unauthorized.html','r')
						file_info = file.read()
						file.close()
						final_output = data + file_info
						connectionSocket.send(final_output.encode())
						logging.debug(f"{ip}:{PortNo} \"{obj.filename} Incorrect Username or Password")
						logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent}")
						logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
						return
				else:
					status = '403'
					forbidden = "HTTP/1.1 "+status+"\n"
					forbidden += "Date: "+curr_time()+"\n"
					forbidden += "Server: Apache/2.4.41(ubuntu)\n"
					forbidden += "Content-Length: "+fileLength("403_Forbidden.html") +"\n"
					forbidden += "Connection: close\n"
					forbidden += "Content-Type: text/html\n\n"
					file = open('403_Forbidden.html','r')
					file_info = file.read()
					file.close()
					final_output = forbidden + file_info
					connectionSocket.send(final_output.encode())
					logging.debug(f"{ip}:{PortNo} \"Requested File {obj.filename} was Forbidden")
					logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
					logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
					return
			else:
				status = '404'
				not_found = "HTTP/1.1 "+status+"\n"
				not_found += "Date: "+curr_time()+"\n"
				not_found += "Server: Apache/2.4.41(ubuntu)\n"
				not_found += "Host: " + str("127.0.0.1") + ":" + str(PortNo) + "\n"
				not_found += "Content-Length: "+ fileLength('404_NotFound.html')+"\n"
				not_found += "Content-Location: "+Location('404_NotFound.html')+"\n"
				not_found += "Content-Type: "+type('404_NotFound.html')+"\n\n"
				file = open('404_NotFound.html','r')
				file_info = file.read()
				file.close()
				final_output = not_found + file_info
				connectionSocket.send(final_output.encode())
				logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
				logging.debug(f"{ip}:{PortNo} \"{obj.filename} File Not Found ")
				logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
				return
		elif obj.method_type == 'PUT':
			if obj.Content_Length:
				if len(obj.data) < MAX_PAYLOAD:
					if (os.path.isfile(obj.filename)):
						if(os.access(obj.filename, os.R_OK) and os.access(obj.filename, os.W_OK)):
							status = '200'
							Writing_format(obj.filename,obj.data)
							final_output = headers(obj.filename,status,obj)
							connectionSocket.send(final_output.encode())
							logging.debug(f"{ip}:{PortNo} \"{obj.filename} File Modified Successfully.")
							logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
							logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
							return
						else:
							status = '403'
							forbidden = "HTTP/1.1 "+status+"\n"
							forbidden += "Date: "+curr_time()+"\n"
							forbidden += "Server: Apache/2.4.41(ubuntu)\n"
							forbidden += "Content-Length: "+fileLength("403_Forbidden.html") +"\n"
							forbidden += "Connection: close\n"
							forbidden += "Content-Type: text/html\n\n"
							file = open('403_Forbidden.html','r')
							file_info = file.read()
							file.close()
							final_output = forbidden + file_info
							connectionSocket.send(final_output.encode())
							logging.debug(f"{ip}:{PortNo} \"Requested File {obj.filename} was Forbidden")
							logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
							logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
							return
					else:
						status = '201'
						Writing_format(obj.filename,obj.data)
						final_output = headers(obj.filename,status,obj)
						connectionSocket.send(final_output.encode())
						logging.debug(f"{ip}:{PortNo} \"{obj.filename} File Created Successfully.")
						logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
						logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
						return
				else:	
					status = '413'
					payload = "HTTP/1.1 "+status+"\n"
					payload += "Date: "+curr_time()+"\n"
					payload += "Server: Apache/2.4.41(ubuntu)\n"
					payload += "Content-Length: "+fileLength("413_Payload.html") +"\n"
					payload += "Connection: close\n"
					payload += "Content-Type: text/html\n\n"
					file = open('413_Payload.html','r')
					file_info = file.read()
					file.close()
					final_output = payload + file_info
					connectionSocket.send(final_output.encode())
					logging.debug(f"{ip}:{PortNo} \"Requested Entity {obj.filename} Too Large")
					logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
					logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
					return
			else:
				status = '411'
				length = "HTTP/1.1 "+status+"\n"
				length += "Date: "+curr_time()+"\n"
				length += "Server: Apache/2.4.41(ubuntu)\n"
				length += "Host: " + str("127.0.0.1") + ":" + str(PortNo) + "\n"
				length += "Content-Length: "+ fileLength('411_Length.html')+"\n"
				length += "Content-Location: "+Location('411_Length.html')+"\n"
				length += "Content-Type: "+type('411_Length.html')+"\n\n"
				file = open('411_Length.html','r')
				file_info = file.read()
				file.close()
				final_output = length + file_info
				connectionSocket.send(final_output.encode())
				logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
				logging.debug(f"{ip}:{PortNo} \"{obj.filename} Content-Length header is required ")
				logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
				return
		elif obj.method_type == 'POST':
			if obj.Content_Length:
				if len(obj.data) < MAX_PAYLOAD:
					if (os.path.isfile(obj.filename)):
						if(os.access(obj.filename, os.R_OK) and os.access(obj.filename, os.W_OK)):
							obj.filename = post_rename(obj.filename)
							status = '200'
							Writing_format(obj.filename,obj.data)
							final_output = headers(obj.filename,status,obj)
							connectionSocket.send(final_output.encode())
							logging.debug(f"{ip}:{PortNo} \"{obj.filename} File Modified and renamed Successfully.")
							logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
							logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
							return
						else:
							status = '403'
							forbidden = "HTTP/1.1 "+status+"\n"
							forbidden += "Date: "+curr_time()+"\n"
							forbidden += "Server: Apache/2.4.41(ubuntu)\n"
							forbidden += "Content-Length: "+fileLength("403_Forbidden.html") +"\n"
							forbidden += "Connection: close\n"
							forbidden += "Content-Type: text/html\n\n"
							file = open('403_Forbidden.html','r')
							file_info = file.read()
							file.close()
							final_output = forbidden + file_info
							connectionSocket.send(final_output.encode())
							logging.debug(f"{ip}:{PortNo} \"Requested File {obj.filename} was Forbidden")
							logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
							logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
							return
					else:
						status = '201'
						Writing_format(obj.filename,obj.data)
						final_output = headers(obj.filename,status,obj)
						connectionSocket.send(final_output.encode())
						logging.debug(f"{ip}:{PortNo} \"{obj.filename} File Created Successfully.")
						logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
						logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
						return
				else:	
					status = '413'
					payload = "HTTP/1.1 "+status+"\n"
					payload += "Date: "+curr_time()+"\n"
					payload += "Server: Apache/2.4.41(ubuntu)\n"
					payload += "Content-Length: "+fileLength("413_Payload.html") +"\n"
					payload += "Connection: close\n"
					payload += "Content-Type: text/html\n\n"
					file = open('413_Payload.html','r')
					file_info = file.read()
					file.close()
					final_output = payload + file_info
					connectionSocket.send(final_output.encode())
					logging.debug(f"{ip}:{PortNo} \"Requested Entity {obj.filename} Too Large")
					logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
					logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
					return
			else:
				status = '411'
				length = "HTTP/1.1 "+status+"\n"
				length += "Date: "+curr_time()+"\n"
				length += "Server: Apache/2.4.41(ubuntu)\n"
				length += "Host: " + str("127.0.0.1") + ":" + str(PortNo) + "\n"
				length += "Content-Length: "+ fileLength('411_Length.html')+"\n"
				length += "Content-Location: "+Location('411_Length.html')+"\n"
				length += "Content-Type: "+type('411_Length.html')+"\n\n"
				file = open('411_Length.html','r')
				file_info = file.read()
				file.close()
				final_output = length + file_info
				connectionSocket.send(final_output.encode())
				logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
				logging.debug(f"{ip}:{PortNo} \"{obj.filename} Content-Length header is required ")
				logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent} ")
				return
	else:
		status = '405'
		allowed = "HTTP/1.1 "+status+"\n"
		allowed += "Date: "+curr_time()+"\n"
		allowed += "Server: Apache/2.4.41(ubuntu)\n"
		allowed += "Content-Length: "+fileLength("405_NotAllowed.html") +"\n"
		allowed += "Connection: close\n"
		allowed += "Allow: GET,HEAD,DELETE,PUT,POST"+"\n"
		allowed += "Content-Type: text/html\n\n"
		file = open("405_NotAllowed.html","r")
		file_info = file.read()
		file.close()
		final_output = allowed + file_info
		connectionSocket.send(final_output.encode())
		logging.debug(f"{ip}:{PortNo} \"{obj.method_type}  Method is Not Allowed.")
		logging.warning(f"{ip}:{PortNo} \"{obj.method_type} /{obj.filename} {obj.http_version}\"{status} {obj.UserAgent}")
		logging.info(f"{ip}:{PortNo} \"{obj.method_type} {obj.http_version} {obj.filename}\"{status} ")
		return

def recieve(connectionSocket):
	connectionSocket.setblocking(0)
	while True:
		try:
			recv = connectionSocket.recv(8192)
			if recv != bytes('','utf-8'):
				all_methods(recv)

		except:
			continue
		
def stop_start(Socket):
	while True:
		string = input()
		string = string.lower()
		if(string == "stop"):
			print("Server stopped")
			Socket.close()
			os._exit(os.EX_OK)
			break		
	
Socket = socket(AF_INET,SOCK_STREAM)
Socket.bind(('',PortNo))
Socket.listen(10)
logging_levels(log_level)
th1 = threading.Thread(target = stop_start, args = (Socket, ))
th1.start()
print(f'Server is ready to receive on localhost:{PortNo}\n')
while True:
		connectionSocket, addr = Socket.accept()
		print(f'Receiving Request from:{addr}')
		
		if(threading.active_count() < MAX_REQUEST):
			th = threading.Thread(target = recieve, args = (connectionSocket, ))
			th.start()
		else:
			
			status = "503"
			randomTime = random.randint(10, 600)
			service = f"HTTP/1.1 "+status+"\n"
			service += "Date: "+curr_time()+"\n"
			service += "Server: Apache/2.4.41(ubuntu)\n"
			service += f"Retry-After: {randomTime}"+"\n"
			service += "Content-Length: "+fileLength("503_ServiceUnavailable.html") +"\n"
			service += "Connection: close\n"
			service += "Content-Type: text/html\n\n"
			file = open('503_ServiceUnavailable.html', "r")
			file_info = file.read()
			file.close()
			final_output = service + file_info
			connectionSocket.send(final_output.encode())
			logging.debug(f"{ip}:{PortNo} \"{MAX_REQUEST} Max requests Limit reached Now service is Unavailable.")
			connectionSocket.close()
			break

