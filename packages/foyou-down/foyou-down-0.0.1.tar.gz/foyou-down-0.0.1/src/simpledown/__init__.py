__version__ = '0.0.1'

import logging
import os
import re
from urllib import parse

import coloredlogs
import requests
import urllib3
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning


class SimpleDown:
    """下载相关"""

    # DOWNLOAD_CHUNK_SIZE = 1024 * 1024 * 10  # 10MB
    DOWNLOAD_CHUNK_SIZE = 1024 * 1024  # 10MB

    @staticmethod
    def get_url_suffix(url) -> str:
        return os.path.splitext(parse.urlparse(url).path)[1]

    @staticmethod
    def get_url_name(url) -> str:
        return os.path.basename(parse.urlparse(url).path)

    @staticmethod
    def ok_name(name: str) -> str:
        """替换字符串中的特殊字符"""
        name = name.replace('\\', '＼')
        name = name.replace('/', '／')
        name = name.replace(':', '：')
        name = name.replace('*', '⁕')
        name = name.replace('?', '？')
        name = name.replace('"', '”')
        name = name.replace('<', '＜')
        name = name.replace('>', '＞')
        name = name.replace('|', '¦')
        name = re.sub(r'\s+', ' ', name)
        return name

    def __init__(self, folder='.'):
        urllib3.disable_warnings(InsecureRequestWarning)

        self.folder = folder
        self.log = logging.getLogger(f'{__name__}')
        # noinspection SpellCheckingInspection
        coloredlogs.install(
            level=logging.DEBUG,
            logger=self.log,
            milliseconds=True,
            datefmt='%X',
            fmt=f'%(asctime)s.%(msecs)03d %(levelname)s %(message)s'
        )
        self.session = requests.session()
        self.session.trust_env = False
        self.session.verify = False

    def get_url_size(self, url: str) -> int:
        with self.session.get(url, stream=True) as resp:
            body_size = int(resp.headers.get('content-length', 0))
            return body_size

    @staticmethod
    def add_serial_number(x):
        return '(' + str(int(x.group()[1:-1]) + 1) + ')'

    @staticmethod
    def get_new_file_path(file_dir, file_name):
        while True:
            file_path = os.path.join(file_dir, file_name)
            if not os.path.exists(file_path):
                return file_path
            name, ext = os.path.splitext(file_name)
            new_name = re.sub(r'\(\d+\)$', SimpleDown.add_serial_number, name)
            if new_name == name:
                new_name = name + '(1)'
            file_name = f'{new_name}{ext}'

    def download(self, url: str, file: str = None) -> str:
        """下载文件"""
        if file is None:
            file = self.get_url_name(url)
        file_path = os.path.join(self.folder, file)

        file_dir, file_name = os.path.split(os.path.abspath(file_path))
        file_name = re.sub(r'[\\/:*?"<>|]', '_', file_name)
        file_path = os.path.join(file_dir, file_name)

        # url 为空判断
        if not url:
            self.log.error(f'文件 {file_path} 下载失败: 获取的url为空, 文件可能被屏蔽导致无法下载')
            return file_path

        self.log.info(f'开始下载文件 {file_path}')

        if os.path.exists(file_path):
            self.log.warning(f'文件已存在 {file_path}')
            if os.path.getsize(file_path) == self.get_url_size(url):
                self.log.warning(f'文件大小相同，跳过下载 {file_path}')
                return file_path
            else:
                file_path = SimpleDown.get_new_file_path(file_dir, file_name)
                self.log.warning(f'文件大小不同，另存为 {file_path}')

        # 递归创建目录
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        tmp_file = file_path + '.tmp'

        tmp_size = 0
        if os.path.exists(tmp_file):
            tmp_size = os.path.getsize(tmp_file)

        try:
            progress_bar = None
            with self.session.get(url, headers={
                'Range': f'bytes={tmp_size}-'
            }, stream=True) as resp:
                body_size = int(resp.headers.get('content-length', 0))
                if resp.headers.get('Accept-Ranges', None) != 'bytes':
                    if tmp_size == 0:
                        self.log.warning(f'此链接不支持断点续传 {resp.url}')
                    else:
                        raise f'此链接不支持断点续传 {resp.url}'
                progress_bar = tqdm(total=body_size + tmp_size, unit='B', unit_scale=True, colour='#31a8ff')
                progress_bar.update(tmp_size)
                with open(tmp_file, 'ab') as f:
                    for content in resp.iter_content(chunk_size=self.DOWNLOAD_CHUNK_SIZE):
                        progress_bar.update(len(content))
                        f.write(content)
            os.renames(tmp_file, file_path)
        finally:
            if progress_bar:
                progress_bar.close()

        self.log.info(f'文件下载完成 {file_path}')
        return file_path


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Python 简单下载器',
        epilog=f'pydown({__version__}) by foyou(https://github.com/foyoux)'
    )
    parser.add_argument('url', nargs='*', help='下载连接')
    parser.add_argument('-f', '--file', dest='file', help='下载连接')
    parser.add_argument('-o', '--out', dest='out', help='下载连接')
    parser.add_argument('-v', '--version', dest='version', help='显示版本号', action="store_true")

    args = parser.parse_args()

    if args.version:
        print('pydown version', __version__)
        return

    url = args.url
    if url is None:
        parser.print_usage()
        return

    out = args.out
    if out is None:
        out = '.'

    SimpleDown(out).download(url, args.file)
