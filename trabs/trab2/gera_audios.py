import wave
import struct
import math
import os

def gerar_som(arquivo, frequencia, duracao=1.0, taxa_amostragem=44100):
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    wave_file = wave.open(arquivo, 'w')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(taxa_amostragem)

    for i in range(int(duracao * taxa_amostragem)):
        valor = int(32767.0 * math.sin(2.0 * math.pi * frequencia * i / taxa_amostragem))
        dados = struct.pack('<h', valor)
        wave_file.writeframesraw(dados)
        
    wave_file.close()

if __name__ == "__main__":
    gerar_som('assets/audios/som1.wav', 261.63)
    gerar_som('assets/audios/som2.wav', 293.66)
    gerar_som('assets/audios/som3.wav', 329.63)
    gerar_som('assets/audios/som4.wav', 349.23)