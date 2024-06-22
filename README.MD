# ![image](src/logo.png) 易思 EASe CHAT https://img.shields.io/badge/toy-ChattingApp-blue
易思是一款基于Kivy架构的跨平台即时聊天应用程序，面向组织内部通讯需求，基于TCP可靠数据传输服务，帮助各类组织内部沟通更加高效安全。产品支持中英双语操作界面，提供基本的聊天功能，包括文字、图片、文件的发送，并且支持设备间文件互传功能。

## 文件结构
```
├── README.MD
├── SDL2.dll
└── src
    ├── __init__.py
    ├── backend
    │   ├── __init__.py
    │   ├── apis.py
    │   ├── clients.py
    │   └── utils.py
    ├── fonts
    ├── frontend
    │   ├── AuthcodeScreen.py
    │   ├── ChatScreen.py
    │   ├── LoginScreen.py
    │   ├── MainScreen.py
    │   ├── __init__.py
    │   ├── background.jpg
    │   ├── demo.py
    │   └── utils.py
    ├── logo.png
    ├── execute.py
    └── server.py
```
## 环境要求
```
python                    3.10.14
kivy                      2.3.0
```

## 程序运行
对于服务器端，使用python运行`src/server.py`，对于客户端，使用python运行`src/execute.py`即可启动交互式聊天页面。
```sh
python src/server.py
python src/execute.py
```
注意：中文输入法弹出输入框需要将系统环境变量默认路径下的SDL2.dll替换为CHAT根目录下的SDL2ddl。
替换后初次运行需要较长时间，请耐心等待。

## 效果展示
https://github.com/dhmbb2/CHAT/assets/123251854/a1618b34-8b4a-47da-9088-07aaa2f65ede
