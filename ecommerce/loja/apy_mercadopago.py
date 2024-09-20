import mercadopago

public_key = "APP_USR-a45e2926-2e0c-4f21-92de-1570d9019c9b"

token = "APP_USR-5638531740701786-091618-14ef03ce13e1282811c117f4bd099f7c-1992597355"


# Substitua 'YOUR_ACCESS_TOKEN' pelo seu token de acesso
sdk = mercadopago.SDK(token)

# Dados da preferência
preference_data = {
    "items": [
        {
            "title": "My Item",
            "quantity": 1,
            "unit_price": 75.76
        }
    ],
    "back_urls":{
      "success": link,
      "pending": link,
      "failure": link,
    }
}

# Criação da preferência
resposta = sdk.preference().create(preference_data)
link = resposta["response"]["init_point"]
id_pagamento = resposta["response"]["id"]
print(link)
# print(resposta)