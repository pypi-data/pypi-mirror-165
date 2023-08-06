# foyou-http
python mini http server

## 快速入门

安装

```shell
pip install -U foyou-http
```

> 关于库名：因为这属于偏向个人的库，为了尽可能不占用公共资源，所有库名看上去有些啰嗦。以后我开发的类似库，都会添加 **foyou-** 前缀。

安装完后会有一个命令行工具 - `pyhttp`

```shell
$ pyhttp --help

usage: pyhttp [-h] [--host HOST] [--port PORT] [--version] [dir]

simple http server for share files.

positional arguments:
  dir          HTTP Server 共享目录

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  HTTP Server 监听地址
  --port PORT  HTTP Server 监听端口
  --version    打印版本信息

pyhttp(0.0.1) by foyou(https://github.com/foyoux)
```

