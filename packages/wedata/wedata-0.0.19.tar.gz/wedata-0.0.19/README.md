# wedata的使用方法

## 安装wedata
```shell
pip install wedata
```

## 本地调用
本地调用需要通过同步工具将数据文件保存在本地后再调用接口进行数据查询


执行命令
```python
import wedata as we
client = we.LocalClient(path="XXX/XXX/XXX")    # path为数据文件的保存根目录
param = {
    'domain': 'descriptor',
    'phylum': 'feature',
    'class': 'aindexeodprices',
    'fields': [],
    'user': '0000001',
    'case': 'equity_20220628',
    'start_date': '20220628',
    'end_date': '20220630',
    'codes': [],
    'form': 'normal'
}
client.query(param)
```

## 远程调用
执行命令
```python
import wedata as we
we.login(username='XXX', password='XXX')
param = {
    'domain': 'descriptor',
    'phylum': 'feature',
    'class': 'aindexeodprices',
    'fields': [],
    'user': '0000001',
    'case': 'equity_20220628',
    'start_date': '20220628',
    'end_date': '20220630',
    'codes': [],
    'form': 'normal'
}
we.query(param)
```
