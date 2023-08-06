import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class telamon():
    
    def scan(url , port):
        
 
        try:
            s.connect((url , port))
            print("[+] Port is OPEN>> "+str(port))
        except:
            print("[-] Port is CLOSED>> "+str(port))
    
    def scanmulti(url , minport , maxport):
       
        for Port in range(minport, maxport + 1):
            try:
                s.connect((url , Port))
                print("[+] Port is OPEN>> "+str(Port))
            
            except:
                print("[-] Port is CLOSED>> "+str(Port))   


    def scanall(url):
        for Port in range(1,6112):
            try:
                s.connect((url , Port))
                print("[+] Port is OPEN>> "+str(Port))
            
            except:
                print("[-] Port is CLOSED>> "+str(Port))
