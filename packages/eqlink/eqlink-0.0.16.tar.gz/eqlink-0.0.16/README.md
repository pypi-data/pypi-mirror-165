# eqlink
基于Python，简单的注册中心框架（为eqsmart服务）。
```
# eqsmart 框架地址
https://github.com/enqiangjing/eqsmart
```

## 1. 使用说明
```shell script
pip install eqlink
```

### 1.1 启动注册中心
```python
import socket
from eqlink.main.server import LinkServer


'''本机IP'''
HOST = socket.gethostname()
'''配置信息'''
SERVER_CONF = {
    'HOST': HOST,
    'PORT': 7878,
    'BUF_SIZE': 1024,
    'BACKLOG': 5
}
LinkServer(SERVER_CONF, './server_list').server_init()

```
### 1.2 示例工程
```
# 注册中心服务 eqlink-server
https://github.com/enqiangjing/eqlink-server
```


## * 免责声明
* 本项目所有内容仅供参考和学习交流使用。
* 项目所存在的风险将由使用者自行承担，因使用本项目而产生的一切后果也由使用者自己承担。
* 凡以任何方式直接、间接使用本项目的人员，视为自愿接受本项目声明和法律法规的约束。