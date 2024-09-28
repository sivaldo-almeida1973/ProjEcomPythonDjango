import mercadopago

public_key = "APP_USR-a45e2926-2e0c-4f21-92de-1570d9019c9b"
token = "APP_USR-5638531740701786-091618-14ef03ce13e1282811c117f4bd099f7c-1992597355"


def criar_pagamento(itens_pedido, link):
    # Substitua 'YOUR_ACCESS_TOKEN' pelo seu token de acesso
    sdk = mercadopago.SDK(token)

    #itens que ele está comprando no formato de dicionario
    itens = []
    for item in itens_pedido:
        quantidade = int(item.quantidade)
        nome_produto = item.item_estoque.produto.nome
        preco_unitario = float(item.item_estoque.produto.preco)
        itens.append({
            "title": nome_produto,
            "quantity": quantidade,
            "unit_price": preco_unitario,
        })


    # Dados da preferência
    preference_data = {
        "items":itens,
        "back_urls":{
        "success": link,
        "pending": link,
        "failure": link,
        }
    }

    # Criação da preferência
    resposta = sdk.preference().create(preference_data)
    link_pagamento = resposta["response"]["init_point"]
    id_pagamento = resposta["response"]["id"]
    return link_pagamento, id_pagamento
   