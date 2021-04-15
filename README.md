# NFC-e API

Objetivo desse projeto foi desenvolver uma simples API para recuperar informações de Notas Fiscais Eletrônicas (NFC-e), já que, quando acessamos o link do QRCode de uma nota fiscal, nos deparamos com uma página HTML.

- Atenção: essa API foi testada e validada somente com notas fiscais dos estados de Sergipe e São Paulo (provavelmente funciona em outros estados também). Porém, constatamos que não funciona com notas fiscais do estado da Paraíba.

- A API está disponível publicamente no host da Vercel: https://nfce-api.vercel.app/nfce

- Para consultar uma nota fiscal acrescente o parâmetro qrcode: https://nfce-api.vercel.app/nfce?qrcode=<link do qrcode>

- Por exemplo, para o seguinte QRCode: http://www.nfce.se.gov.br/portal/qrcode.jsp?p=28200339346861004078650140001369591140797433%7C2%7C1%7C1%7C6A7F6793C8B5E1AE4B1B153A1A259FA26644F92D

- Você deve acessar o seguinte link: https://nfce-api.vercel.app/nfce?qrcode=http://www.nfce.se.gov.br/portal/qrcode.jsp?p=28200339346861004078650140001369591140797433%7C2%7C1%7C1%7C6A7F6793C8B5E1AE4B1B153A1A259FA26644F92D

- Assim, você recupera os dados em JSON, conforme mostrado abaixo
```sh
{
  "nfce": {
    "chave": "2820 0339 3468 6100 4078 6501 4000 1369 5911 4079 7433", 
    "data": "16/03/2020 15:24:11", 
    "empresa": {
      "cnpj": "39.346.861/0040-78", 
      "endereco": "Av Silvio Teixeira, 831, Jardins, Aracaju, SE", 
      "nome": "CENCOSUD BRASIL COMERCIAL LTDA"
    }, 
    "itens": [
      {
        "cod": "119478702", 
        "ord": 1, 
        "qtde": 0.854, 
        "tit": "BATATA MINI EMB KG KG", 
        "un": "KG", 
        "vl_sem_desconto": 3.24, 
        "vl_unit": 3.79
      }, 
      {
        "cod": "165303502", 
        "ord": 2, 
        "qtde": 2.112, 
        "tit": "FRAN RESF FREG KG KG", 
        "un": "KG", 
        "vl_sem_desconto": 17.21, 
        "vl_unit": 8.15
      }, 
      {
        "cod": "121505002", 
        "ord": 3, 
        "qtde": 0.755, 
        "tit": "CARRE SUIN BISTCKG KG", 
        "un": "KG", 
        "vl_sem_desconto": 8.98, 
        "vl_unit": 11.89
      }, 
      {
        "cod": "174456700100", 
        "ord": 4, 
        "qtde": 1.0, 
        "tit": "SABAO PO OMO BAG UN", 
        "un": "UN", 
        "vl_sem_desconto": 19.15, 
        "vl_unit": 19.15
      }
    ], 
    "link": "http://www.sefaz.se.gov.br/nfce/consulta", 
    "qrcode": "http://www.nfce.se.gov.br/portal/qrcode.jsp?p=28200339346861004078650140001369591140797433|2|1|1|6A7F6793C8B5E1AE4B1B153A1A259FA26644F92D", 
    "qtde_itens": 4, 
    "total_com_desconto": 48.58, 
    "total_desconto": 0.0, 
    "total_sem_desconto": 48.58
  }
}
```

Para rodar a API localmente no seu computador:

- Clone ou faça o download deste repositório

- Rode os seguintes comandos no seu terminal 
```sh
pip install -r requirements.txt
python nfce-api.py 
```

- E utilize o seguinte link http://127.0.0.1:5000/nfce?qrcode=<link do qrcode>
