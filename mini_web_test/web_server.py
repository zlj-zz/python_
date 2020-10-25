# coding=utf-8
import socket
import re
import multiprocessing
# import dynamic.mini_frame
import sys


class WSGIServer(object):
    def __init__(self, port, app, static_path):
        # 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM)
        # 设置当前服务器先close，即4次挥手后资源能立即释放，保证下次可以立即相应
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET,
                                          socket.SO_REUSEADDR, 1)

        # 绑定端口
        self.tcp_server_socket.bind(("", port))
        # 变为监听套接字
        self.tcp_server_socket.listen(128)

        self.application = app
        self.static_path = static_path

    def service_client(self, new_socket):
        # 接受客户端发来数据
        request = new_socket.recv(1024).decode("utf-8")
        # 获取请求文件名
        request_lines = request.splitlines()
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])

        if ret:
            file_name = ret.group(1)
            # print(file_name)
            # print("*"*20)
        # print(file_name.endswith(".html"))
        # 非.py结尾 就认为为静态资源
        if not file_name.endswith(".html"):
            try:
                with open(self.static_path + file_name, "rb") as fb:
                    html_content = fb.read()
                # http格式
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                # 发送header和数据
                new_socket.send(response.encode("utf-8"))
                new_socket.send(html_content)
            except:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "<h1 align='center'>-----file not found-----</h1>"
                new_socket.send(response.encode("utf-8"))
        else:
            env = dict()
            env['PATH_INFO'] = file_name
            # body = dynamic.mini_frame.application(env, self.set_response_header)
            body = self.application(env, self.set_response_header)

            header = 'HTTP/1.1 %s\r\n' % self.status
            for temp in self.headers:
                header += "%s:%s\r\n" % (temp[0], temp[1])
            header += '\r\n'

            response = header + str(body)
            new_socket.send(response.encode('utf-8'))

        # 关闭监听套接字
        new_socket.close()

    def set_response_header(self, status, headers):
        self.status = status
        self.headers = [("Server: mini")]
        self.headers += headers

    def run_forever(self):
        while True:
            # 等待客户端连接
            new_socket, client_addr = self.tcp_server_socket.accept()
            p = multiprocessing.Process(target=self.service_client,
                                        args=(new_socket, ))
            p.start()

            new_socket.close()

        # 关闭监听套接字
        self.tcp_server_socket.close()


def main():
    if len(sys.argv) == 3:
        try:
            port = int(sys.argv[1])
            fram_app_name = sys.argv[2]
        except Exception as e:
            print("port error")

        ret = re.match(r"([^:]+):(.*)", fram_app_name)
        if ret:
            fram_name = ret.group(1)
            app_name = ret.group(2)
        else:
            print("格式出错---(python3 xxx.py port fram_name:fction)")

        with open("./web_server.conf") as f:
            conf_info = eval(f.read())

        sys.path.append(conf_info['dynamic_path'])
        frame = __import__(fram_name) # 返回值标记导入模块
        app = getattr(frame, app_name) #返回值指向模块函数

        wsgi_server = WSGIServer(port, app, conf_info['static_path'])
        wsgi_server.run_forever()

        wsgi_server.run_forever()

    else:
        print("格式出错---(python3 xxx.py port fram_name:fction)")
    """控制整体"""


if __name__ == '__main__':
    main()
