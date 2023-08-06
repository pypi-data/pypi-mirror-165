import socket
class DtptcCli:
    def __init__(self) -> None:
        self.defaultcon =["127.0.0.1",12345]
    def GetLen(self,channel):
        self.cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.cli.connect(tuple(self.defaultcon))
        self.cli.send(f"getlen-{channel}-".ljust(100,"0").encode())
        l=self.cli.recv(100)
        self.cli.close()
        return l.split(b"-")
    def GetData(self,channel):
        self.cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.cli.connect(tuple(self.defaultcon))
        self.cli.send(f"getdata-{channel}-".ljust(100,"0").encode())
        ld = self.cli.recv(100)
        gt = ld.split(b"-")
        if ld.find(b"ok")==-1:
            self.cli.close()
            return [True,gt]
        else:
            dg=self.cli.recv(int(gt[1]))
            self.cli.close()
            return [False,dg]

    def SendData(self,channel,data):
        self.cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.cli.connect(tuple(self.defaultcon))
        self.cli.sendall(f"senddata-{channel}-{len(data)}-".ljust(100,"0").encode())
        self.cli.sendall(data)
        ld=self.cli.recv(100)
        self.cli.close()
        return ld.split(b"-")

if __name__=="__main__":
    xe = DtptcCli()
    lz=xe.SendData(1,b"2333")
    print(lz)
    lz=xe.SendData(1,b"2444")
    print(lz)
    b = xe.GetData(1)
    print(b)
    z = xe.GetLen(1)
    print(z)
# cc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# #推送数据
# #获取数据
# def SendData():
#     ...
# def GetData():
#     ...
# #-->连接获取database数据长度-->发送数据到服务端
# cc.connect(("127.0.0.1",2333))
# while True:
#     b=cc.recv(2333)
#     if b==b'':
#         break
#     else:
#         print(b)