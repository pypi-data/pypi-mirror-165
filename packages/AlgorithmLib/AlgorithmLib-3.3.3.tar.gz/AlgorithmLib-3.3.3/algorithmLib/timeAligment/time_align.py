import ctypes
import sys
from ctypes import *
from formatConvert import wav2pcm


class delaystruct(Structure):
 _fields_ = [

        ("Crude_DelayEst", c_long),  # c_byte

 ]

def cal_delay(reffile, testfile, samplerate):
        delays = delaystruct()

        import platform
        mydll = None
        cur_paltform = platform.platform().split('-')[0]
        if cur_paltform == 'Windows':
            mydll = ctypes.windll.LoadLibrary(sys.prefix + '/time_align.dll')
        if cur_paltform == 'macOS':
            mydll = CDLL(sys.prefix + '/time_align.dylib')

        inputFile = c_char_p(
               bytes(reffile.encode('utf-8')))  # create_unicode_buffer(inFile.encode('utf-8'), len(inFile))
        outputFile = c_char_p(
               bytes(testfile.encode('utf-8')))  # create_unicode_buffer(outFile.encode('utf-8'), len(outFile))
        if samplerate == 8000:
               mode = 'nb'
        if samplerate == 16000:
               mode = 'wb'
        cmode = c_char_p(bytes(mode.encode('utf-8')))
        mydll.cal_delay(inputFile, outputFile, samplerate, cmode, byref(delays))
        print(delays.Crude_DelayEst)
        return delays.Crude_DelayEst

if __name__ == '__main__':
       ref = r'C:\Users\vcloud_avl\Documents\我的POPO\src.wav'
       test = r'C:\Users\vcloud_avl\Documents\我的POPO\test.wav'
       cal_delay(wav2pcm(ref),wav2pcm(test),48000)
       pass