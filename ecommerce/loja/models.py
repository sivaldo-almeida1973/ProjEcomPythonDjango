from django.db import models

# Create your models here.
# bases de dados(tabelas)

#Cliente
   # nome
   #email
   #telefone
   #usuario

#Produto
   # imagem
   # nome
   # preco
   # ativo
   #categoria
   # tipo



# Categorias
    #nome


# Tipos 
    #nome


# ItemEstoque
    # produto(ex: camisa)
    # cor(ex: azul, laranja, verde)
    # tamanho (ex: P, M, G)
    # quantidade



# ItensPedido
    # itemestoque
    # quantidade


#Pedido
    # cliente
    # data_finalizacao
    # finalizado
    # id_transacao
    # endereco
    # itenspedido

#Endereco 
    # rua
    # numero
    # complemento
    # cep
    # cidade
    # estado
    # cliente



