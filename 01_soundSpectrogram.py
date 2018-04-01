#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# MORIUMIUS スペシャルサイエンスプログラム　音解析
# Sound Spectrogram
# バージョン 1.0  Edited by Jun Komachi(2018/3/21)
# matplotlib等のライブラリはできるだけ最新のバージョンを使ってください
# pip install -U matplotlib でバージョンアップ可能です
# 参考ホームページ
# http://own-search-and-study.xyz/2017/10/27/pythonを使って音声データからスペクトログラムを作/
# http://own-search-and-study.xyz/2017/05/18/pythonのmatplotlibでgifアニメを作成する/
# http://nalab.mind.meiji.ac.jp/~mk/labo/text/python/node30.html
# https://qiita.com/itoru257/items/8af2902d8ce851ae74ea
# pipでインストールしたライブラリ pydub, seaborn
# pydubを使うには FFmpegが必要（設定が面倒）
# FFmpeg https://evermeet.cx/ffmpeg/
# 実行パスを通しておいてください(.bash_profileや.cshrcなど)
# オーディオファイル形式はwav, mp3, ogg, flv, m4a, mp4, wma, aac等に対応しているようです
# 音源ファイル
# https://www.onosokki.co.jp/HP-WK/nakaniwa/keisoku/bugs_sound.htm
# http://www.bekkoame.ne.jp/~sibutaka/nature/html/insects/00_insectsounds_b_j.html
import os
from pydub import AudioSegment
import numpy as np
np.set_printoptions(threshold=np.inf)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

opt = argparse.ArgumentParser(description='Sound Spectrogram')
opt.add_argument('-f', action='store', dest='file', required=True,
                 help='Input audio file')
opts = opt.parse_args()
base, ext = os.path.splitext(opts.file)
ext = ext.split('.')
#print 'extention='+str(ext)
sound = AudioSegment.from_file(opts.file, ext[1])

channel = sound.channels
rate    = sound.frame_rate
time    = sound.duration_seconds
#print 'Channels = ' + str(channel)
#print 'Freq rate = ' + str(rate)
#print 'Time = ' + str(time)

# ステレオの片方の音だけ抽出する
samples = np.array(sound.get_array_of_samples())
#print samples
sample  = samples[::sound.channels]
#print sample
#plt.plot(sample[::10])
#plt.show()

# フーリエ変換してスペクトルを抽出
#spectrum = np.fft.fft(sample)

# 窓幅
w = 1000
# 刻み幅
s = 500
# スペクトル格納用
ampList = []
# 偏角格納用
argList = []

# 刻みずつずらしながら窓幅分のデータをフーリエ変換する
for i in range(int((sample.shape[0] - w)/s)):
    data = sample[i*s:i*s+w]
    spectrum = np.fft.fft(data)
    spectrum = spectrum[:int(spectrum.shape[0]/2)]
    spectrum[0] = spectrum[0] / 2
    ampList.append(np.abs(spectrum))
    argList.append(np.angle(spectrum))

# 周波数は共通なので1回だけ計算（縦軸表示に使う）
freq = np.fft.fftfreq(data.shape[0], 1.0/sound.frame_rate)
freq = freq[:int(freq.shape[0]/2)]
# 時間も共通なので1回だけ計算（横軸表示に使う）
time = np.arange(0, i+1, 1) * s / sound.frame_rate

# 使いやすさのためにnumpy配列にしておく
ampList = np.array(ampList)
argList = np.array(argList)

# 周波数を可視化するため、pandasのデータを作る
df_amp = pd.DataFrame(data=ampList, index=time, columns=freq)

# seabornのheatmapを使う
plt.figure(figsize=(10,6))
sns.heatmap(data=np.log(df_amp.iloc[:, :200].T),
            xticklabels=100,
            yticklabels=10,
            cmap=plt.cm.gist_rainbow_r
            )
plt.show()

# 偏角を可視化
#df_arg = pd.DataFrame(data=argList, index=time, columns=freq)
#
#plt.figure(figsize=(20,6))
#sns.heatmap(data=df_arg.iloc[:, :100].T,
#            xticklabels=100,
#            yticklabels=10,
#            cmap=plt.cm.gist_rainbow_r,
#            )
#plt.show()
