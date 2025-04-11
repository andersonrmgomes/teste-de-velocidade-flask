document.addEventListener('DOMContentLoaded', function() {
    const pingBtn = document.getElementById('pingBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const uploadBtn = document.getElementById('uploadBtn');
    const pingResult = document.getElementById('pingResult');
    const downloadResult = document.getElementById('downloadResult');
    const uploadResult = document.getElementById('uploadResult');
    const statusMessage = document.getElementById('statusMessage');
    const gaugeValue = document.querySelector('.gauge-value');
    
    // Arquivo para teste de upload (gera 100MB de dados aleatórios)
    function createTestFile(size) {
        const buffer = new ArrayBuffer(size);
        const view = new Uint8Array(buffer);
        for (let i = 0; i < view.length; i++) {
            view[i] = Math.floor(Math.random() * 256);
        }
        return new Blob([buffer], {type: 'application/octet-stream'});
    }
    
    // Teste de ping
    pingBtn.addEventListener('click', function() {
        setStatus('Medindo ping...');
        disableButtons(true);
        updateGauge(0);
        
        const startTime = performance.now();
        
        fetch('/ping_test')
            .then(response => response.json())
            .then(data => {
                pingResult.textContent = data.ping;
                setStatus('Ping concluído!');
            })
            .catch(error => {
                console.error('Erro no teste de ping:', error);
                setStatus('Erro ao medir ping.');
            })
            .finally(() => {
                disableButtons(false);
            });
    });
    
    // Teste de download
    downloadBtn.addEventListener('click', function() {
        setStatus('Iniciando teste de download...');
        disableButtons(true);
        updateGauge(0);
        
        const startTime = performance.now();
        let fileSize = 0;
        
        fetch('/download_test')
            .then(response => {
                // Obter o tamanho do arquivo do cabeçalho Content-Length
                fileSize = parseInt(response.headers.get('Content-Length') || '0');
                
                // Configurar reader para medir progresso
                const reader = response.body.getReader();
                let receivedLength = 0;
                let chunks = [];
                
                return new Promise((resolve, reject) => {
                    function processResult(result) {
                        if (result.done) {
                            // Concluído
                            const endTime = performance.now();
                            const downloadTime = (endTime - startTime) / 1000; // em segundos
                            
                            // Enviar resultados para o servidor para cálculo
                            fetch('/measure_download', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    file_size: fileSize,
                                    time: downloadTime
                                }),
                            })
                            .then(response => response.json())
                            .then(data => {
                                downloadResult.textContent = data.download_speed;
                                updateGauge(data.download_speed);
                                setStatus(`Download concluído! Velocidade: ${data.download_speed} Mbps`);
                            });
                            
                            resolve();
                            return;
                        }
                        
                        // Recebeu um pedaço do arquivo
                        const chunk = result.value;
                        chunks.push(chunk);
                        receivedLength += chunk.length;
                        
                        // Atualizar progresso
                        const percentComplete = Math.round((receivedLength / fileSize) * 100);
                        setStatus(`Baixando... ${percentComplete}% concluído`);
                        
                        // Continuar lendo
                        return reader.read().then(processResult);
                    }
                    
                    // Iniciar leitura
                    reader.read().then(processResult);
                });
            })
            .catch(error => {
                console.error('Erro no teste de download:', error);
                setStatus('Erro ao testar download.');
            })
            .finally(() => {
                disableButtons(false);
            });
    });
    
    // Teste de upload
    uploadBtn.addEventListener('click', function() {
        setStatus('Preparando arquivo para upload...');
        disableButtons(true);
        updateGauge(0);
        
        // Criar um arquivo de teste de 25MB (menor para upload)
        const fileSize = 25 * 1024 * 1024; // 25 MB
        setStatus('Gerando arquivo de teste...');
        
        // Gerar arquivo em chunks para não travar a interface
        setTimeout(() => {
            const testFile = createTestFile(fileSize);
            
            setStatus('Iniciando upload...');
            const formData = new FormData();
            formData.append('file', testFile);
            
            const startTime = performance.now();
            
            // Enviar o arquivo para o servidor
            fetch('/upload_test', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                uploadResult.textContent = data.upload_speed;
                updateGauge(data.upload_speed);
                setStatus(`Upload concluído! Velocidade: ${data.upload_speed} Mbps`);
            })
            .catch(error => {
                console.error('Erro no teste de upload:', error);
                setStatus('Erro ao testar upload.');
            })
            .finally(() => {
                disableButtons(false);
            });
        }, 100);
    });
    
    // Funções auxiliares
    function setStatus(message) {
        statusMessage.textContent = message;
    }
    
    function disableButtons(disabled) {
        pingBtn.disabled = disabled;
        downloadBtn.disabled = disabled;
        uploadBtn.disabled = disabled;
    }
    
    function updateGauge(value) {
        gaugeValue.textContent = value;
    }
});
