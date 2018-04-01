#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# MORIUMIUS スペシャルサイエンスプログラム　音声ファイルトリミング
# Sound Trimming
# バージョン 1.0  Edited by Jun Komachi(2018/3/30)
import os
from pydub import AudioSegment
import argparse

opt = argparse.ArgumentParser(description='Sound file trimming')
opt.add_argument('-f', action='store', dest='file', required=True,
                 help='Input audio file')
opt.add_argument('--first', action='store', dest='first_millisecond', type=int, default=0,
                 help='Trimming first part of file by millisecond')
opt.add_argument('--last', action='store', dest='last_millisecond', type=int, default=0,
                 help='Trimming last part of file by millisecond')
opts = opt.parse_args()
base, ext = os.path.splitext(opts.file)
ext = ext.split('.')
#print 'extention='+str(ext)
sound = AudioSegment.from_file(opts.file, ext[1])

# 冒頭部分,最終部分の切り取り
new = sound[opts.first_millisecond:-opts.last_millisecond]

# ファイルの保存
new.export(base+'_new.'+str(ext[1]), format=ext[1])
