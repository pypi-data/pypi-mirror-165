#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : 陈坤泽
# @Email  : 877362867@qq.com
# @Date   : 2021/08/25 15:57

from collections import defaultdict

import cv2
from tqdm import tqdm

from pyxllib.file.specialist import get_etag
from pyxllib.cv.xlcvlib import CvImg, xlcv
from pyxllib.cv.xlpillib import PilImg, xlpil
from pyxllib.file.specialist import XlPath


def __1_目录级处理图片的功能():
    pass


class ImagesDir(XlPath):
    def debug_image_func(self, func, pattern='*', *, save=None, show=False):
        """
        :param func: 对每张图片执行的功能，函数应该只有一个图片路径参数  new_img = func(img)
            当函数有多个参数时，可以用lambda函数技巧： lambda im: func(im, arg1=..., arg2=...)
        :param save: 如果输入一个目录，会将debug结果图存储到对应的目录里
        :param show: 如果该参数为True，则每处理一张会imshow显示处理效果
            此时弹出的窗口里，每按任意键则显示下一张，按ESC退出
        :return:

        TODO 显示原图、处理后图的对比效果
        TODO 支持同时显示多张图处理效果
        """
        if save:
            save = XlPath(save)

        for f in self.glob_images(pattern):
            im1 = xlcv.read(f)
            im2 = func(im1)

            if save:
                xlcv.write(im2, self / save / f.name)

            if show:
                xlcv.imshow2(im2)
                key = cv2.waitKey()
                if key == '0x1B':  # ESC 键
                    break

    def reduce_image_filesize(self, pattern='*',
                              limit_size=4 * 1024 ** 2, *,
                              read_flags=None,
                              change_length=True,
                              suffix=None,
                              print_mode=True):
        """ 减小图片尺寸，可以限制目录里尺寸最大的图片不超过多少

        :param limit_size: 限制的尺寸
            一般自己的相册图片，亲测300kb其实就够了~~，即 300 * 1024
            百度API那边，好像不同接口不太一样，4M、6M、10M等好像都有
                但百度那是base64后的尺寸，会大出1/3
                为了够用，
        :param read_flags: 读取图片时的参数，设为1，可以把各种RGBA等奇怪的格式，统一为RGB
        :param change_length: 默认是要减小图片的边长，尺寸，来压缩图片的
            可以设为False，不调整尺寸，纯粹读取后再重写，可能也能压缩不少尺寸
        :param suffix: 可以统一图片后缀格式，默认保留原图片名称
            要带前缀'.'，例如'.jpg'
            注意其他格式的原图会被删除

        因为所有图片都会读入后再重新写入，速度可能会稍慢
        """

        def printf(*args, **kwargs):
            if print_mode:
                print(*args, **kwargs)

        printf('原始大小', self.size(human_readable=True))

        for f in tqdm(self.glob_images(pattern), disable=not print_mode):
            im = xlpil.read(f, read_flags)
            _suffix = suffix or f.suffix
            if change_length:
                im = xlpil.reduce_filesize(im, limit_size, _suffix)
            xlpil.write(im, f.with_suffix(_suffix))
            if f.suffix != _suffix:
                f.delete()

        printf('新目录大小', self.size(human_readable=True))

    def adjust_image_shape(self, pattern='*', min_length=None, max_length=None, print_mode=True):
        def printf(*args, **kwargs):
            if print_mode:
                print(*args, **kwargs)

        j = 1
        for f in self.glob_images(pattern):
            # 用pil库判断图片尺寸更快，但处理过程用的是cv2库
            h, w = xlpil.read(f).size[::-1]
            x, y = min(h, w), max(h, w)

            if (min_length and x < min_length) or (max_length and y > max_length):
                im = xlcv.read(f)
                im2 = xlcv.adjust_shape(im, min_length, max_length)
                if im2.shape != im.shape:
                    printf(f'{j}、{f} {im.shape} -> {im2.shape}')
                    xlcv.write(im2, f)
                    j += 1

    def glob_repeat_images(self, pattern='*', *, sort_mode='count', print_mode=False):
        """ 返回重复的文件组

        :param sort_mode:
            count: 按照重复的文件数量从多到少排序
            size: 按照空间总占用量从大到小排序
        :return: [(etag, files, per_file_size), ...]
        """
        from pyxllib.cv.imhash import phash

        # 1 获取所有etag，这一步比较费时
        hash2files = defaultdict(list)
        for f in tqdm(self.glob_images(pattern), desc='get image phash', disable=not print_mode):
            im_phash = phash(str(f))
            hash2files[im_phash].append(f)

        # 2 转格式，排序
        hash2files = [(k, vs, vs[0].size()) for k, vs in hash2files.items() if len(vs) > 1]
        if sort_mode == 'count':
            hash2files.sort(key=lambda x: (-len(x[1]), -len(x[1]) * x[2]))
        elif sort_mode == 'size':
            hash2files.sort(key=lambda x: (-len(x[1]) * x[2], -len(x[1])))

        # 3 返回每一组数据
        return hash2files

    def delete_repeat_images(self, pattern='*', *, sort_mode='count', print_mode=True, debug=False):
        """ 检查、删除可能重复的图片

        :param debug:
            True，只是输出检查清单，不做操作
            False, 保留第1个文件，删除其他文件
            TODO，添加其他删除模式
        :param print_mode:
            TODO 支持html富文本显示，带超链接
        """
        from humanfriendly import format_size

        def printf(*args, **kwargs):
            if print_mode:
                print(*args, **kwargs)

        files = self.glob_repeat_images(pattern, sort_mode=sort_mode, print_mode=print_mode)
        for i, (etag, files, _size) in enumerate(files, start=1):
            n = len(files)
            printf(f'{i}、{etag}\t{format_size(_size)} × {n} ≈ {format_size(_size * n)}')

            for j, f in enumerate(files, start=1):
                if debug:
                    printf(f'\t{f.relpath(self)}')
                else:
                    if j == 1:
                        printf(f'\t{f.relpath(self)}')
                    else:
                        f.delete()
                        printf(f'\t{f.relpath(self)}\tdelete')
            if print_mode:
                printf()
