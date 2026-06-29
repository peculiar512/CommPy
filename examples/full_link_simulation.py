目录结构
CommPy/
├─ commpy/          # 框架源码文件夹
│  └─ modulation/  # 各类调制算法存放处
├─ examples/        # 示例脚本文件夹（我们在这里新建文件）
└─ docs/
模块化封装
import numpy as np
import matplotlib.pyplot as plt
from commpy.modulation import PSKModem, QAMModem
from commpy.channelcoding import HammingCodec
from commpy.channels import awgn, rayleigh_fading

def communication_full_chain(
    n_bits: int,
    snr_db: float,
    mod_type: str = "bpsk",
    channel_type: str = "awgn",
    hamming: bool = True
):
    """
    一键运行完整数字通信收发链路
    :param n_bits: 发送原始比特总数
    :param snr_db: 信道信噪比dB
    :param mod_type: bpsk / 16qam
    :param channel_type: awgn / rayleigh
    :param hamming: 是否开启汉明码信道编码
    :return: 误码率BER
    """
    # ========== 1. 信源：生成随机二进制比特流 ==========
    bits = np.random.randint(0, 2, size=n_bits)

    # ========== 2. 信道编码：汉明(7,4)编码 ==========
    if hamming:
        hamming_encoder = HammingCodec(7, 4)
        # 补齐比特长度适配汉明码分组
        pad_len = (4 - len(bits) % 4) % 4
        bits_pad = np.pad(bits, (0, pad_len), mode="constant")
        coded_bits = hamming_encoder.encode(bits_pad)
    else:
        coded_bits = bits

    # ========== 3. 数字调制 ==========
    if mod_type.lower() == "bpsk":
        modem = PSKModem(2)  # M=2即BPSK
    elif mod_type.lower() == "16qam":
        modem = QAMModem(16)
    else:
        raise ValueError("仅支持 bpsk / 16qam")
    mod_symbols = modem.modulate(coded_bits)

    # ========== 4. 信道传输：AWGN / 瑞利衰落 ==========
    if channel_type == "awgn":
        rx_symbols = awgn(mod_symbols, snr_db)
    elif channel_type == "rayleigh":
        # 瑞利平坦衰落 + 加噪声
        fade_coeff = rayleigh_fading(mod_symbols.shape)
        faded_sig = mod_symbols * fade_coeff
        rx_symbols = awgn(faded_sig, snr_db)

    # ========== 5. 解调 ==========
    demod_bits = modem.demodulate(rx_symbols, demod_type="hard")

    # ========== 6. 信道译码 ==========
    if hamming:
        decoded_bits = hamming_encoder.decode(demod_bits)
        decoded_bits = decoded_bits[:n_bits]  # 去掉补位比特
    else:
        decoded_bits = demod_bits[:n_bits]

    # ========== 7. 误码统计BER ==========
    bit_err = np.sum(bits != decoded_bits)
    ber = bit_err / n_bits
    return ber

# ===================== 一键入口：主运行函数 =====================
if __name__ == "__main__":
    # 遍历多个SNR绘制BER曲线
    snr_list = np.arange(0, 12, 2)
    ber_result = []
    for snr in snr_list:
        ber = communication_full_chain(
            n_bits=10000,
            snr_db=snr,
            mod_type="bpsk",
            channel_type="awgn",
            hamming=True
        )
        ber_result.append(ber)
        print(f"SNR={snr}dB, BER={ber:.6e}")

    # 绘图
    plt.semilogy(snr_list, ber_result, "-o", label="BPSK+Hamming AWGN信道")
    plt.xlabel("SNR (dB)")
    plt.ylabel("误码率 BER")
    plt.grid(True, which="both")
    plt.legend()
    plt.show()
