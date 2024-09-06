from django.db.models import Max, Min

def filtra_produtos(produtos, filtro):
    if filtro: 
        if "-" in filtro:
            categoria, tipo = filtro.split("-")  #
            produtos = produtos.filter(tipo__slug=tipo, categoria__slug=categoria)
        else:    
            produtos = produtos.filter(categoria__slug=filtro)
    return produtos


def preco_minimo_maximo(produtos):
    minimo = 0
    maximo = 0
    if len(produtos) > 0: 
        maximo = list(produtos.aggregate(Max("preco")).values())[0]
        maximo = round(maximo, 2)
        minimo = list(produtos.aggregate(Min("preco")).values())[0]
        minimo = round(minimo, 2)
    return minimo, maximo


def ordenar_produtos(produtos, ordem):
    if ordem == "menor-preco":
        produtos = produtos.order_by("preco")
    elif ordem == "maior-preco":
        produtos = produtos.order_by("-preco")#decrescente
    elif ordem == "mais-vendidos":
        lista_produtos = []
        for produto in produtos:
            lista_produtos.append((produto.total_vendas(), produto))
        lista_produtos = sorted(lista_produtos, reverse=True)
        produtos = [item[1] for item in lista_produtos]
        # print(lista_produtos)
        #     # print(produto.nome, produto.total_vendas())
   
    return produtos
