import httpx
import json
import os

headers = {
    'Host': 'sandbox.clicksign.com',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

params = {"access_token": "7e9dc98f-3e49-4d90-a7f1-ada90f427b01"}

modelo_contrato = '6dc3b20a-a347-4074-b6ce-9aeb4edb84fa'

url = f'https://sandbox.clicksign.com/api/v1/templates/{modelo_contrato}/documents?'

data = json.dumps({
    "document": {
        "path": "/contratos/TIC_YYYYMMDDhhmmss_22233344455.pdf",
        "template": {
            "data": {
                "idDiretorio": "1234567",
                "nome": "TIC_YYYYMMDD_CPFgestorQueConvidou",
                "descricao": "Termo de inclusão de contatos",
                "dataValidade": "",
                "extensao": "pdf",
                "tipoArquivo": 293
      }
    }
  }
})

response = httpx.post(
    url = url,
    data = data,
    headers = headers,
    params = params)

chave = response.json()['document']['key']
print(response.json())
print(chave)



