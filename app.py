from flask import Flask, render_template, jsonify, request, send_file
import time
import os
import random
import string
import numpy as np
import io

app = Flask(__name__)

# Tamanho do arquivo de teste em bytes (100 MB)
TEST_FILE_SIZE = 100 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_test')
def download_test():
    # Gerar um nome de arquivo único
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.bin'
    
    # Criar buffer em memória
    buffer = io.BytesIO()
    
    # Gerar conteúdo do arquivo diretamente no buffer
    chunk_size = 1024 * 1024  # 1 MB por chunk
    chunks = TEST_FILE_SIZE // chunk_size
    remainder = TEST_FILE_SIZE % chunk_size
    
    # Preencher o buffer com zeros
    zeros = np.zeros(chunk_size, dtype=np.uint8).tobytes()
    for _ in range(chunks):
        buffer.write(zeros)
    if remainder > 0:
        buffer.write(np.zeros(remainder, dtype=np.uint8).tobytes())
    
    buffer.seek(0)  # Resetar posição do buffer
    
    # Enviar o buffer como arquivo
    return send_file(
        buffer,
        as_attachment=True,
        download_name=file_name,
        mimetype='application/octet-stream'
    )

@app.route('/upload_test', methods=['POST'])
def upload_test():
    start_time = time.time()
    file = request.files['file']
    
    # Usar buffer em memória para o upload
    file_buffer = io.BytesIO()
    file.save(file_buffer)
    file_buffer.seek(0)
    
    # Calcular tamanho e velocidade
    file_size = len(file_buffer.getvalue())
    upload_time = time.time() - start_time
    upload_speed = (file_size * 8) / upload_time / 1_000_000  # Mbps
    
    return jsonify({
        'upload_speed': round(upload_speed, 2),
        'file_size': file_size,
        'time': round(upload_time, 2)
    })

@app.route('/measure_download', methods=['POST'])
def measure_download():
    data = request.json
    file_size = data.get('file_size', 0)
    download_time = data.get('time', 0)
    
    if download_time > 0:
        download_speed = (file_size * 8) / download_time / 1_000_000  # Mbps
        return jsonify({
            'download_speed': round(download_speed, 2),
            'file_size': file_size,
            'time': round(download_time, 2)
        })
    else:
        return jsonify({'error': 'Tempo de download inválido'}), 400

@app.route('/ping_test')
def ping_test():
    start_time = time.time()
    time.sleep(0.001)  # Simula processamento mínimo
    latency = (time.time() - start_time) * 1000  # em ms
    return jsonify({'ping': round(latency, 2)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
