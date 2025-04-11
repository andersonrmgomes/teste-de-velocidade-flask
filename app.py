from flask import Flask, render_template, jsonify, request, send_file
import time
import os
import random
import string
import numpy as np

app = Flask(__name__)

# Diretório para armazenar o arquivo de teste
TEST_FILE_DIR = 'test_files'
if not os.path.exists(TEST_FILE_DIR):
    os.makedirs(TEST_FILE_DIR)

# Tamanho do arquivo de teste em bytes (100 MB)
TEST_FILE_SIZE = 100 * 1024 * 1024

# Gerar um arquivo de teste com zeros (mais eficiente que dados aleatórios)
def generate_test_file(file_path, size):
    with open(file_path, 'wb') as f:
        # Criar um array de zeros e escrevê-lo no arquivo
        zeros = np.zeros(min(size, 1024 * 1024), dtype=np.uint8)
        remaining = size
        while remaining > 0:
            write_size = min(remaining, zeros.size)
            f.write(zeros[:write_size].tobytes())
            remaining -= write_size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_test')
def download_test():
    # Gerar um nome de arquivo único
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.bin'
    file_path = os.path.join(TEST_FILE_DIR, file_name)
    
    # Gerar o arquivo de teste
    generate_test_file(file_path, TEST_FILE_SIZE)
    
    # Enviar o arquivo
    return send_file(file_path, as_attachment=True)

@app.route('/upload_test', methods=['POST'])
def upload_test():
    start_time = time.time()
    file = request.files['file']
    
    # Salvar o arquivo temporariamente
    temp_path = os.path.join(TEST_FILE_DIR, 'temp_upload.bin')
    file.save(temp_path)
    
    # Calcular o tamanho do arquivo
    file_size = os.path.getsize(temp_path)
    
    # Calcular o tempo e a velocidade
    upload_time = time.time() - start_time
    upload_speed = (file_size * 8) / upload_time / 1_000_000  # Mbps
    
    # Limpar arquivo temporário
    os.remove(temp_path)
    
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
    # Simula um pequeno atraso de processamento
    time.sleep(0.001)
    latency = (time.time() - start_time) * 1000  # em ms
    
    return jsonify({
        'ping': round(latency, 2)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
