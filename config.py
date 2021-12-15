import sys

# localhost
ip = '127.0.0.1'

# Port Number input from the user
PortNo = int(sys.argv[1])

# Log level input from the user (level1 -> user,level2 -> debug ,level3 -> developer)
log_level = (sys.argv[2])

# Only these five HTTP Methods are allowed 
Allow = ["GET","HEAD","DELETE","PUT","POST"]

# Max Payload for Put and Post
MAX_PAYLOAD = 100000

# Max connections at a time
MAX_REQUEST = 50

# Max URI Length
MAX_LENGTH = 25

# Username and Password for Authentication in Delete Method
USERNAME = 'Vishal'
PASSWORD = 'Vishal@235'

# HTTP verions supported
Http_versions =['HTTP/1.1','HTTP/1.0']

# Media type supported
media = ['text/html', 'text/css', 'text/plain', 'text/csv',
                'application/pdf', 'application/json', 'audio/mpeg',
                'image/jpeg', 'image/png', 'image/gif', 'video/mp4']