import sys
import subprocess
import pkg_resources
import json
import os
from datetime import datetime
import logging

if not os.path.isdir("logs"):
    os.mkdir("logs")

logname =  datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

logging.basicConfig(filename= "logs/"+logname+".log", 
					format='%(levelname)s - %(asctime)s - %(message)s',
					filemode='w') 
logger=logging.getLogger()
logger.setLevel(logging.INFO)
logger.warning("Log Iniciado")

if not os.path.isdir("temp"):
    os.mkdir("temp")
    logger.warning("Criado Diretorio TEMP")


required = {'pdfkit'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
try:
    if missing:
        logger.warning("Necessário pdfkit")
        logging.info("nstalando Pacotes")
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
        logging.info("pdfkit isntalado")
except:
    logger.error("Falha ao instalar o pdfkit")
    exit()

try:
    import pdfkit
except ImportError as e:
    logging.error("Falha ao importar paocte pdfkit")
    exit()

nomeArquivoOrigem = input("Digite caminho do arquivo Json: ")

logging.info("Carregando Arquivos")
arquivoJson = open(nomeArquivoOrigem,'r',encoding='utf8')
modelo = open('./models/ReciboModels.html','r',encoding='utf8')
modeloLista = open('./models/listProdutosModels.html','r',encoding='utf8')

logging.info("Carregando Json")
dados = json.load(arquivoJson)

logging.info("Gerando Recibo")
recibo = modelo.read()
modelo.close()
recibo = recibo.replace("{{NOME}}",dados['nome'])
recibo = recibo.replace("{{CNPJ}}",dados['cnpj'])
recibo = recibo.replace("{{INSCRIÇÃOESTADUAL}}",dados['inscricaoEstadual'])
recibo = recibo.replace("{{ENDERECO}}",dados['endereco'])
recibo = recibo.replace("{{TELEFONE}}",dados['telefone'])
recibo = recibo.replace("{{EMAIL}}",dados['email'])

logging.info("Gerando Lista de Produtos")
reciboLista = modeloLista.read()
modeloLista.close()
listaProdutos = ""
for item in dados['produtos']:
    intemlista = reciboLista
    intemlista = intemlista.replace("{{DATAEXPEDICAO}}",item['dataExpedicao'])
    intemlista = intemlista.replace("{{NOTAFISCAL}}",item['notaFiscal'])
    intemlista = intemlista.replace("{{PRODUTO}}",item['produto'])
    intemlista = intemlista.replace("{{LOTE}}",item['lote'])
    intemlista = intemlista.replace("{{QUANTIDADE}}",item['quantidade'])
    listaProdutos = listaProdutos+intemlista
recibo = recibo.replace("{{LINHA}}",listaProdutos)

logging.info("Gerando Arquivo TEMP")
arquivoTemporario = open("temp/temp.html", "a",encoding='utf8')
arquivoTemporario.write(recibo)
arquivoTemporario.close()

logging.info("Criado PDF")
optionsPdf = {
    'page-size':'A4',
    'encoding':'utf-8', 
    'margin-top':'0.5cm',
    'margin-bottom':'0cm',
    'margin-left':'0.4cm',
    'margin-right':'0cm'
}
pdfkit.from_file('/temp/temp.html', nomeArquivoOrigem[:-4]+"pdf", options=optionsPdf)

logging.info("Limpando arquivo temporario")

os.remove("temp/temp.html")

arquivoJson.close()

input("\nPresione [Enter] para sair")