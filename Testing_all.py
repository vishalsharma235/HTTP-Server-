from socket import *
import threading
import sys
import os

ip = '127.0.0.1'
PortNo = int(sys.argv[1])

def main():    
    putMethod_thread = threading.Thread(target=PUT_Method_Testing("hello.txt"))
    putMethod_thread.start()
    putMethod_thread.join()

    postMethod_thread = threading.Thread(target=POST_Method_Testing("world.txt"))
    postMethod_thread.start()
    postMethod_thread.join()

    getTesting_thread = threading.Thread(target=GET_Method_Testing("hello.txt"))
    getTesting_thread.start()
    getTesting_thread.join()
    
    headTesting_thread = threading.Thread(target=HEAD_Method_Testing("world.txt"))
    headTesting_thread.start()
    headTesting_thread.join()

    deleteTesting_thread = threading.Thread(target=DELETE_Method_Testing("world.txt"))
    deleteTesting_thread.start()
    deleteTesting_thread.join()

    unauthorizedTesting_thread = threading.Thread(target=UNAUTHORIZED_Testing("hello.txt"))
    unauthorizedTesting_thread.start()
    unauthorizedTesting_thread.join()

    os.chmod('hello.txt', 0o000)
    file_permissions("hello.txt")

    forbiddenTesting_thread = threading.Thread(target=FORBIDDEN_Testing("hello.txt"))
    forbiddenTesting_thread.start()
    forbiddenTesting_thread.join()

    os.chmod('hello.txt', 0o777)
    file_permissions("hello.txt")

    deleteTesting_thread = threading.Thread(target=DELETE_Method_Testing("hello.txt"))
    deleteTesting_thread.start()
    deleteTesting_thread.join()

    unsupportedMediType_thread = threading.Thread(target=UNSUPPORTED_Media_Type_Testing("any.py"))
    unsupportedMediType_thread.start()
    unsupportedMediType_thread.join()

    methodNotAllowed_thread = threading.Thread(target=METHOD_Not_Allowed_Testing("hey.txt"))
    methodNotAllowed_thread.start()
    methodNotAllowed_thread.join()

    versionNotSupported_thread = threading.Thread(target=VERSION_Not_Supported_Testing("hey.txt"))
    versionNotSupported_thread.start()
    versionNotSupported_thread.join()

    uriTooLong_thread = threading.Thread(target=URI_Too_Long_Testing("file/get/uri_too_long/hello/world/file.txt"))
    uriTooLong_thread.start()
    uriTooLong_thread.join()

def GET_Method_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'GET /{file} HTTP/1.1\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: 8bcd1632-afba-4da2-84ff-ef6bcbf58a7b\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    Data = Socket.recv(12000)
    print("\nGET Method Testing:\n")
    print(Recieve.decode())
    print('File_Content:',Data.decode())
    Socket.close()

def HEAD_Method_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'HEAD /{file} HTTP/1.1\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: 010544dd-7ca9-4b78-a4a6-094cdd9fcc72\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nHEAD Method Testing:\n")
    print(Recieve.decode())
    Socket.close()

def DELETE_Method_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'DELETE /{file} HTTP/1.1\r\nAuthorization: Basic VmlzaGFsOlZpc2hhbEAyMzU=\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: 86b8feee-4e25-4894-91db-954e45416903\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nDELETE Method Testing:\n")
    print(Recieve.decode())
    Socket.close()

def UNAUTHORIZED_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'DELETE /{file} HTTP/1.1\r\nAuthorization: Basic VmlzaGFsOlZpc2hhbEAyMw==\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: d0a83e9a-037e-4d19-a04f-638293b1f160\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nDELETE Method(Unauthorized):\n")
    print(Recieve.decode())
    Socket.close()

def FORBIDDEN_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'GET /{file} HTTP/1.1\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: 9339d533-7de9-4da6-8698-5f7b1e661e34\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nFORBIDDEN Testing:\n")
    print(Recieve.decode())
    Socket.close()

def UNSUPPORTED_Media_Type_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'GET /{file} HTTP/1.1\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: feb97d8d-f7b1-4677-82d5-bc4d609102b0\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nUNSUPPORTED_Media_Type Testing:\n")
    print(Recieve.decode())
    Socket.close()

def METHOD_Not_Allowed_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'PATCH /{file} HTTP/1.1\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: a148d0a7-9041-41c5-94e5-ec3e6b69fa6d\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 0\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nMETHOD_Not_Allowed Testing:\n")
    print(Recieve.decode())
    Socket.close()

def VERSION_Not_Supported_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'GET /{file} HTTP/2.1\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: 8bcd1632-afba-4da2-84ff-ef6bcbf58a7b\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nVERSION_Not_Supported Testing:\n")
    print(Recieve.decode())
    Socket.close()

def PUT_Method_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'PUT /{file} HTTP/1.1\r\nContent-Type: text/plain\r\nUser-Agent: Self_Testing\r\nAccept: */*\r\nPostman-Token: f3dae9c7-dbad-4fb8-8431-9c7a0ccc726e\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 21\r\n\r\ndata stored in a file'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nPUT Method Testing:\n")
    print(Recieve.decode())
    Socket.close()

def POST_Method_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'POST /{file} HTTP/1.1\r\nContent-Type: text/plain\r\nUser-Agent: Self_Testing\r\nAccept: */*\r\nPostman-Token: 3fb035b4-fce9-4d10-852f-fd02ac0232e5\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 22\r\n\r\nsome data\nhello world'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nPOST Method Testing:\n")
    print(Recieve.decode())
    Socket.close()

def URI_Too_Long_Testing(file):
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.connect((ip,PortNo))
    Request = f'GET /{file} HTTP/1.1\r\nUser-Agent: Self-Testing\r\nAccept: */*\r\nPostman-Token: 8bcd1632-afba-4da2-84ff-ef6bcbf58a7b\r\nHost: localhost:{PortNo}\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'
    Socket.send(Request.encode())
    Recieve = Socket.recv(4096)
    print("\nURI_Too_Long Testing:\n")
    print(Recieve.decode())
    Socket.close()

def file_permissions(file):
    print("\nchanging file permissions\n")
    mask = oct(os.stat(file).st_mode)[-3:]
    print(f"File permission mask for {file}: {mask}\n")

main()
