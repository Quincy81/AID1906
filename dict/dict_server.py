"""
dict 服务端

功能：业务逻辑处理
模型：多进程TCP并发
"""
from socket import *
from multiprocessing import *
import signal, sys

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)


# 接受客户端请求，分配处理函数
def request(c):
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ":", data)


# 创建tcp套接字
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(ADDR)
s.listen(3)

# 处理僵尸进程
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

# 循环等待客户端连接
print('Listen to the port 8000')


def main():
    while True:
        try:
            c, addr = s.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务端退出')
        except Exception as e:
            print(e)
            continue

        # 为客户端创建子进程
        p = Process(target=request, args=(c,))
        p.daemon = True
        p.start()


if __name__ == "__main__":
    main()
