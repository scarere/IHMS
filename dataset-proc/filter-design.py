from sk_dsp_comm import fir_design_helper as fir_d
import matplotlib.pyplot as plt
import scipy.signal as sigproc
import wfdb

b_l = fir_d.firwin_kaiser_lpf(8, 50, d_stop=80, fs=1000)
#b_h = fir_d.firwin_kaiser_hpf(0.3, 0.5, d_stop=40, fs=1000)
fir_d.freqz_resp_list([b_l],[1],'dB',fs=1000)

plt.ylim([-100,5])
plt.xlim([0,100])
plt.title(r'Kaiser HPF')
plt.ylabel(r'Filter Gain (dB)')
plt.xlabel(r'Frequency in Hz')
plt.grid();
plt.show()

records = wfdb.get_record_list('ptbdb')
signal, field = wfdb.rdsamp('data/ptb-original-1.0.0/' + records[0])
signal = signal[:, 1]
win = signal[0:1000] # Fs is 1000Hz, therefore a 10s window is 10000 samples
winf = sigproc.filtfilt(b=b_l, a=1, x=win)
print(len(winf))
plt.plot(win)
plt.plot(winf)
plt.show()