from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import urllib.request      
import html
import json
import re

def cleanText(text):
  text = re.sub(r'(\s|\t|\n|\r)+', ' ', text) # spaces and lines
  text = re.sub(r',(\s*),', ',', text) # multiple commas
  return text

def getNumber(text):
    num = re.search(r'((\d|,)+)', text).group(1)
    return num.replace(",",".") 

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def home():
    msg = "Bem-vindo a API da NFC-e! Utilize a URL /nfce e adicione um QRCode como parâmetro para recuperar os dados no formato JSON."
    return jsonify({'message': msg})

@app.route('/nfce', methods=['GET'])
def nota():

    qrcode = request.args.get('qrcode')
    
    if not qrcode:
        msg = "Bem-vindo a API da NFC-e! Adicione um QRCode como parâmetro para recuperar os dados no formato JSON."
        return jsonify({'message': msg})
    
    if not re.search(r'(http.+\?p=.+)', qrcode):
        return jsonify({'error': 400, 'message':'QRCode Inválido'}), 400
        
    try:
        html = urllib.request.urlopen(qrcode).read()
    except (ValueError, urllib.error.URLError):
        return jsonify({'error': 400, 'message':'Requisição Inválida'}), 400
    
    try:
        soup = BeautifulSoup(html, "html.parser")
    
        if soup.find("div",class_="avisoErro"):
            erro = soup.find("div",class_="avisoErro").text.strip()
            return jsonify({'error': 400, 'message':erro}), 400
    
        empresa = soup.find("div", id="conteudo").find("div", class_="txtCenter")
        nome = empresa.find("div", class_="txtTopo").text.strip()
        cnpj = empresa.find_all("div", class_="text")[0].text.strip()
        cnpj = cleanText(cnpj)[6:]
        endereco = empresa.find_all("div", class_="text")[1].text.strip()
        endereco = cleanText(endereco)

        cont = 0
        itens = []
        table = soup.find("table", id="tabResult")
        for row in table.find_all("tr"):
            col1 = row.find_all("td")[0]
            col2 = row.find_all("td")[1]
            item = {}
            item['tit'] = col1.find("span", class_="txtTit").text.strip()
            item['cod'] = getNumber(col1.find("span", class_="RCod").text.strip())
            item['qtde'] = float(getNumber(col1.find("span", class_="Rqtd").text))
            item['un'] = col1.find("span", class_="RUN").text.strip()[4:]
            item['vl_unit'] = float(getNumber(col1.find("span", class_="RvlUnit").text))
            item['vl_sem_desconto'] = float(getNumber(col2.find("span", class_="valor").text))
            cont += 1	
            item['ord'] = cont
            itens.append(item)

        # Totais
        total_div = soup.find("div", id="totalNota").text.lower()
        total_div = cleanText(total_div)
        qtde_itens = int(getNumber(re.search(r'(itens.+)', total_div).group(1)))
        total_com_desconto = float(getNumber(re.search(r'(valor a pagar.+)', total_div).group(1)))
        total_sem_desconto = total_com_desconto
        total_desconto = 0.0
        desconto_re = re.search(r'(desconto.+)', total_div)
        if desconto_re != None:
            total_desconto = float(getNumber(desconto_re.group(1)))
            total_sem_desconto = float(getNumber(re.search(r'(valor total.+)', total_div).group(1)))

        # Acesso
        span_acesso = soup.find("span", class_="chave")
        li_acesso = cleanText(str(span_acesso.parent))
        link_acesso = re.search(r'((http|www)[^<]+)', li_acesso).group(1)
        chave_acesso = re.search(r'chave">(.+)<\/span', li_acesso).group(1)
       
        # Data
        infos_div = soup.find("div", id="infos")
        data = re.search(r'(\d\d\/\d\d\/\d\d\d\d \d\d:\d\d:\d\d)', infos_div.text).group(1)
        
        nfce = {
            'qrcode': qrcode,
            'chave': chave_acesso,
            'link': link_acesso,
            'empresa': {
                'nome':nome,
                'cnpj':cnpj,
                'endereco':endereco},
            'itens':itens,
            'data' : data,
            'qtde_itens' : qtde_itens,
            'total_sem_desconto': total_sem_desconto,
            'total_desconto': total_desconto,
            'total_com_desconto': total_com_desconto
        }
        
        # CPF e Nome
        stg_cpf = infos_div.find("strong", text="CPF: ")
        stg_nome = infos_div.find("strong", text="Nome: ")
        if stg_cpf:
            cpf = stg_cpf.parent.text[6:]
            nfce['pessoa_cpf'] = cpf
        if stg_nome:
            nome = stg_nome.parent.text[7:]
            nfce['pessoa_nome'] = nome
                
        return jsonify({'nfce': nfce})
    
    except Exception as e:
        return jsonify({'error': 400, 'message': str(e)}), 400
        

if __name__ == "__main__":
    app.run(debug=True)