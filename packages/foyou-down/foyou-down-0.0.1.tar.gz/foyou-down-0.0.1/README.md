# foyou-down

python 简单下载库

## 快速入门

安装

```shell
pip install -U foyou-down
```

安装完成后，会有一个 `pydown` 的命令行命令，供 cli 调用，支持断点续传 & 进度显示

作为库调用

```python
from simpledown import SimpleDown

if __name__ == '__main__':
    url = 'https://w.wallhaven.cc/full/72/wallhaven-72rd8e.jpg'
    down = SimpleDown()

    down.download(url)
```