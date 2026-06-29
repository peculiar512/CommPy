"""
BPSK/QPSK/16QAM 在AWGN信道下的误码率对比仿真
作者：peculiar512
"""
import numpy as np
import matplotlib.pyplot as plt
from commpy.modulation import PSKModem, QAMModem
from commpy.channels import awgn
from commpy.utilities import bit_error_rate

# 参数设置
bit_num = 100000  # 仿真比特数
snr_range = np.arange(0, 16, 2)  # 信噪比范围

# 调制方式
modems = {
    'BPSK': PSKModem(2),
    'QPSK': PSKModem(4),
    '16QAM': QAMModem(16)
}

plt.figure(figsize=(8, 5))

for name, modem in modems.items():
    ber_list = []
    bits = np.random.randint(0, 2, bit_num)
    symbols = modem.modulate(bits)
    
    for snr in snr_range:
        rx_symbols = awgn(symbols, snr)
        rx_bits = modem.demodulate(rx_symbols, 'hard')
        ber = bit_error_rate(bits, rx_bits)[0]
        ber_list.append(ber)
    
    plt.semilogy(snr_range, ber_list, marker='o', label=name)

plt.xlabel('SNR (dB)')
plt.ylabel('误码率 BER')
plt.title('不同调制方式在AWGN信道下的误码率性能对比')
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.savefig('examples/ber_curve.png', dpi=300)
plt.show()