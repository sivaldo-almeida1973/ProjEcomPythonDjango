let url = new URL(document.URL);//document pega a url da pagina atual
let itens = document.getElementsByClassName("item-ordenar");
console.log(itens)
//pega elemento de acordo com a classe dele

//para cada item da lista de itens 
for (i = 0; i < itens.length; i++) {
  url.searchParams.set("ordem", itens[i].name);//url recebe como parametro o que esta no name do item(na pagina da loja)
  itens[i].href = url.href;
}

console.log(itens)