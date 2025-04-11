# Teste de Velocidade de Rede com Python e Flask

Este projeto é um sistema simples de teste de velocidade de internet (download, upload e ping) desenvolvido em Python utilizando o framework Flask. Ele mede a largura de banda da rede sem depender de bibliotecas externas, como `speedtest-cli`. O sistema realiza o teste manualmente, transferindo arquivos para calcular as velocidades.

---

## 📋 **Sumário**

- [Descrição do Projeto](#descrição-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 📖 **Descrição do Projeto**

O objetivo deste projeto é criar uma ferramenta educacional e funcional para medir a velocidade da internet. O sistema realiza os seguintes testes:

1. **Ping**: Mede a latência (tempo de resposta) entre o cliente e o servidor.
2. **Download**: Mede a velocidade ao baixar um arquivo gerado pelo servidor diretamente na memória, utilizando buffers (`BytesIO`).
3. **Upload**: Mede a velocidade ao enviar um arquivo do cliente para o servidor, também utilizando buffers em memória.

Os resultados são exibidos em uma interface web simples, que pode ser acessada localmente.

Essa abordagem elimina o uso de arquivos temporários no disco, garantindo maior eficiência e compatibilidade com diferentes sistemas operacionais.


---

## 🚀 **Funcionalidades**

- Medir a latência da rede (ping).
- Testar a velocidade de download utilizando buffers em memória.
- Testar a velocidade de upload utilizando buffers em memória.
- Interface web responsiva e fácil de usar.
- Resultados exibidos em tempo real.

---

## ✅ **Pré-requisitos**

Antes de começar, você precisará ter os seguintes itens instalados na sua máquina:

1. **Python 3.7+**
2. **Pip** (gerenciador de pacotes do Python)
3. **Git** (opcional, para clonar o repositório)

---

## 🛠️ **Instalação**

Siga os passos abaixo para configurar o projeto:

1. Clone este repositório:
~~~~
git clone https://github.com/andersonrmgomes/teste-de-velocidade-flask.git
cd teste-de-velocidade-fl
~~~~

2. Crie um ambiente virtual (opcional, mas recomendado):
~~~~
python -m venv venv
source venv/bin/activate # Linux/MacOS
venv\Scripts\activate # Windows
~~~~

3. Instale as dependências:
~~~~
pip install flask numpy
~~~~

4. Crie a pasta para os arquivos temporários:
~~~~
mkdir test_files
~~~~

---

## ▶️ **Como Executar**

1. Inicie o servidor Flask:
~~~~
python app.py
~~~~

2. Abra o navegador e acesse:
~~~~
http://127.0.0.1:5000
~~~~

3. Use os botões na interface para realizar os testes de ping, download e upload.

---

## 📂 **Estrutura do Projeto**

~~~~
teste-de-velocidade-flask/
├── app.py # Código principal do backend em Flask
├── static/ # Arquivos estáticos (CSS e JS)
│ ├── css/
│ │ └── style.css # Estilo da interface web
│ └── js/
│ └── script.js # Lógica do frontend em JavaScript
├── templates/
│ └── index.html # Página HTML principal
└── test_files/ # Diretório para arquivos temporários usados nos testes (não utilizado com buffers)
~~~~

---

## 🛠️ **Tecnologias Utilizadas**

As principais tecnologias utilizadas neste projeto são:

### Backend:
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Numpy](https://numpy.org/) (para manipulação eficiente de dados)
- [BytesIO](https://docs.python.org/3/library/io.html#io.BytesIO) (para trabalhar com buffers em memória)

### Frontend:
- HTML5, CSS3 e JavaScript

---

## 🤝 **Contribuição**

Contribuições são sempre bem-vindas! Se você tiver sugestões ou melhorias para este projeto:

1. Faça um fork do repositório.
2. Crie uma branch com sua feature ou correção:
~~~~
git checkout -b minha-feature
~~~~
3. Faça commit das suas alterações:
~~~~
git commit -m "Adicionei uma nova funcionalidade"
~~~~
4. Envie para sua branch:
~~~~
git push origin minha-feature
~~~~
5. Abra um Pull Request no GitHub.

---

## 📜 **Licença**

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📧 **Contato**

Se tiver dúvidas ou sugestões, entre em contato:

- Nome: Anderson Gomes
- Email: andersonrmgomes@msn.com
- GitHub: [andersonrmgomes](https://github.com/andersonrmgomes)

---

Agradecemos por conferir este projeto! 🎉
