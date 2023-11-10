document.addEventListener('DOMContentLoaded', function() {
  const generateButton = document.getElementById('generate-btn');
  const textInput = document.getElementById('text-input');

  generateButton.addEventListener('click', function() {
    const text = textInput.value;
    console.log('Sending text to server:', text); // 控制台日志，以便调试

    fetch('https://f351-35-226-109-192.ngrok.io/synthesize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: text })
    })
    .then(response => {
      if (response.ok) {
        console.log('Success:', response);
        return response.blob(); // 假设服务器响应是一个blob
      }
      throw new Error('Network response was not ok.');
    })
    .then(blob => {
      // 创建下载链接
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      // 命名下载文件
      a.download = 'tts_output.wav';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      console.log('Audio file downloaded.');
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });
});
