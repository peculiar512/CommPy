

[![Build Status](https://secure.travis-ci.org/veeresht/CommPy.svg?branch=master)](https://secure.travis-ci.org/veeresht/CommPy)
[![Coverage](https://coveralls.io/repos/veeresht/CommPy/badge.svg?branch=master)](https://coveralls.io/r/veeresht/CommPy)
[![PyPi](https://badge.fury.io/py/scikit-commpy.svg)](https://badge.fury.io/py/scikit-commpy)
[![Docs](https://readthedocs.org/projects/commpy/badge/?version=latest)](http://commpy.readthedocs.io/en/latest/?badge=latest)

MyCommPy
 通信系统仿真工具箱
基于 veeresht/CommPy 二次开发的 Python 数字通信算法工具包，用于通信原理课程学习、算法验证与仿真实验。
一、项目简介
本项目在 CommPy 开源项目的基础上进行扩展与优化，补充了通信工程学习中常用的算法实现、可视化仿真脚本与中文使用文档，降低通信算法的入门门槛，可直接用于课程实验、课程设计与原理验证。
项目完整保留原作者的开源协议与版权声明，所有新增与修改内容均遵循 BSD 3-Clause 开源许可证。
二、主要功能
2.1 原有核心能力（来自原 CommPy 项目）
信道编码：卷积码编译码、Viterbi 译码、MAP 译码、Turbo 码编译码、有限域运算、循环码生成多项式构造
信道模型：SISO/MIMO 瑞利/莱斯衰落信道、二进制删除信道 BEC、二进制对称信道 BSC、AWGN 信道
调制解调：PSK、QAM 调制解调、OFDM 收发信号处理、MIMO 检测算法、对数似然比计算
滤波器：矩形滤波器、升余弦/根升余弦滤波器、高斯滤波器
辅助工具：序列生成、汉明/欧氏距离计算、信号功率计算、上下采样
2.2 新增/优化功能（本次二次开发）
以下内容可根据你实际修改的部分填写，示例如下：
新增 中文注释与算法原理说明，为核心函数补充通信原理层面的参数解释与使用场景
新增 一键式链路仿真脚本，可直接完成「信源-编码-调制-信道-解调-译码-误码统计」完整流程
新增 可视化模块，自动绘制星座图、误码率 BER 曲线、眼图、信道冲击响应图
补充 极化码编译码、载波同步、位同步 等原项目未覆盖的经典通信算法
适配最新版 NumPy/SciPy，修复部分函数的版本兼容问题
新增通信原理课程配套实验示例，包含 BPSK/QPSK/16QAM 性能对比、卷积码编码增益验证等
三、环境依赖
Python 3.8 及以上
NumPy 1.20 及以上
SciPy 1.5 及以上
Matplotlib 3.3 及以上（用于可视化仿真）
SymPy 1.7 及以上
四、安装与使用
4.1 本地安装（使用本修改版本）
克隆或下载本项目到本地
进入项目根目录，执行安装命令：
cd CommPy
python setup.py install
4.2 快速上手示例
示例：绘制 BPSK 调制在 AWGN 信道下的误码率曲线
import numpy as np
import matplotlib.pyplot as plt
from commpy.modulation import PSKModem
from commpy.channels import awgn
from commpy.utilities import bit_error_rate

# 生成随机比特序列
bits = np.random.randint(0, 2, 100000)
# BPSK 调制
psk = PSKModem(2)
symbols = psk.modulate(bits)

# 不同信噪比下的误码率测试
snr_range = np.arange(0, 11, 1)
ber_list = []
for snr in snr_range:
    rx_symbols = awgn(symbols, snr)
    rx_bits = psk.demodulate(rx_symbols, 'hard')
    ber = bit_error_rate(bits, rx_bits)[0]
    ber_list.append(ber)

# 绘制 BER 曲线
plt.semilogy(snr_range, ber_list, marker='o')
plt.xlabel('SNR (dB)')
plt.ylabel('Bit Error Rate')
plt.title('BPSK 在 AWGN 信道下的误码率性能')
plt.grid(True)
plt.show()
五、项目目录结构
CommPy/
├── commpy/              # 核心算法代码
│   ├── channelcoding/   # 信道编码模块
│   ├── channels/        # 信道模型模块
│   ├── modulation/      # 调制解调模块
│   ├── filters/         # 滤波器模块
│   └── utilities/       # 工具函数
├── examples/            # 新增：仿真示例与课程实验脚本
├── docs/                # 新增：中文说明文档
├── README.md            # 项目说明
├── LICENSE              # 开源许可证（完整保留原协议）
└── setup.py             # 安装配置文件
六、更新日志
v1.0.0（个人定制版）
基于原 CommPy 最新版本进行二次开发
新增可视化仿真模块与课程实验示例
补充核心函数的中文注释与使用说明
优化部分函数的运行效率与兼容性
七、致谢与开源声明
原项目信息：本项目基于 veeresht/CommPy 进行二次开发，原作者为 V. Taranalli, B. Trotobas 及贡献者。
开源协议：本项目沿用原项目的 BSD 3-Clause License，完整许可证文本见项目根目录下的 LICENSE 文件。
原项目所有版权归原作者所有，本项目仅用于学习与科研用途，不用于任何商业用途。
八、许可证
BSD 3-Clause License
Copyright (c) 2026 个人定制版本修改者
Copyright (c) 2012-2020 V. Taranalli, B. Trotobas and CommPy contributors
详见 LICENSE 文件。