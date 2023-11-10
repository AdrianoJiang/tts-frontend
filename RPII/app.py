import torch

from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS

# 提前加载模型
tacotron2 = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tacotron2', model_math='fp16')
tacotron2.eval().to('cuda')

waveglow = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_waveglow', model_math='fp16')
waveglow.eval().to('cuda')

utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tts_utils')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    # 获取用户提交的文本
    text = request.json['text']
    # 准备输入序列
    sequences, lengths = utils.prepare_input_sequence([text])

    # 生成mel spectrogram
    with torch.no_grad():
        mel, _, _ = tacotron2.infer(sequences, lengths)

    # 生成音频
    with torch.no_grad():
        audio = waveglow.infer(mel)
    audio_numpy = audio[0].data.cpu().numpy()

    # 保存音频文件
    sf.write('output_audio.wav', audio_numpy, 22050)

    # 返回音频文件
    return send_file('output_audio.wav', mimetype='audio/wav', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)