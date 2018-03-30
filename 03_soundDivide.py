#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# MORIUMIUS スペシャルサイエンスプログラム　音声ファイル分割
# Sound file divider
# バージョン 1.0  Edited by Jun Komachi(2018/3/30)
# matplotlib等のライブラリはできるだけ最新のバージョンを使ってください
# pip install -U matplotlib でバージョンアップ可能です
# 参考ホームページ
# http://chachay.hatenablog.com/entry/2016/10/03/215841

import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import matplotlib.pyplot as plt
import argparse

opt = argparse.ArgumentParser(description='Sound file devider by low volume part')
opt.add_argument('-f', action='store', dest='file', required=True,
                 help='Input audio file')
opts = opt.parse_args()
base, ext = os.path.splitext(opts.file)
ext = ext.split('.')
#print 'extention='+str(ext)
sound = AudioSegment.from_file(opts.file, ext[1])

chunks = split_on_silence(
    sound,

    # 1500ms以上の無音がある場所で分割
    min_silence_len = 1500,

    # -30dBFS以下で無音とみなす
    silence_thresh  = -30,

    # 分割後500msだけ無音を残す
    keep_silence    = 500
)

# 分割数の表示
print 'number of silence divide: ' + str(len(chunks))

# ファイルの保存
for i, chunk in enumerate(chunks):
  chunk.export(base+'_'+str(i)+'.'+str(ext[1]), format=ext[1])
