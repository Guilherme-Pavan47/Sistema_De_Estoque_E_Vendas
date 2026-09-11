from services.estoque_service import EstoqueService




def inteiro(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um numero inteiro valido.")




def decimal(msg):
    while True:
        try:
            return float(input(msg).replace(",", "."))
        except ValueError:
            print("Digite um valor valido.")




def pausa():
    input("\nPressione ENTER para continuar...")




def produto_info(p):
    print(f"Nome: {p.nome}")
    print(f"Codigo: {p.codigo}")
    print(f"Preco: R$ {p.preco:.2f}")
    print(f"Quantidade em estoque: {p.quantidade}")
    print(f"Valor em estoque: R$ {p.preco * p.quantidade:.2f}")




def cliente_info(c):
    print(f"Nome: {c.nome}")
    print(f"Codigo: {c.codigo}")




def listar_produtos(lista):
    if not lista:
        print("Nenhum produto cadastrado.")
        return


    for p in lista:
        print(
            f"Codigo {p.codigo} | {p.nome} | "
            f"Preco: R$ {p.preco:.2f} | "
            f"Estoque: {p.quantidade} | "
            f"Valor: R$ {p.preco * p.quantidade:.2f}"
        )




def listar_clientes(lista):
    if not lista:
        print("Nenhum cliente cadastrado.")
        return


    for c in lista:
        print(f"Codigo {c.codigo} | Nome: {c.nome}")




def listar_vendas(lista, service):
    if not lista:
        print("Nenhuma venda registrada.")
        return


    for v in lista:
        c = service.clientes.buscar(v.codigo_cliente)


        if c:
            cliente = f"{c.nome} (codigo {c.codigo})"
        else:
            cliente = (
                f"Cliente removido "
                f"(codigo {v.codigo_cliente})"
            )


        print(
            f"Venda {v.codigo} | "
            f"Cliente: {cliente} | "
            f"Total: R$ {v.valor_total:.2f}"
        )


        for item in v.itens:
            p = service.produtos.buscar(
                item["codigo_produto"]
            )


            if p:
                nome = p.nome
            else:
                nome = "Produto removido"


            subtotal = (
                item["quantidade"] *
                item["preco_unitario"]
            )


            print(
                f"   -> {nome} "
                f"(codigo {item['codigo_produto']}) | "
                f"Quantidade: {item['quantidade']} | "
                f"Subtotal: R$ {subtotal:.2f}"
            )




def detalhes_venda(v, service):
    c = service.buscar_cliente(v.codigo_cliente)


    print(f"Codigo da venda: {v.codigo}")
    print(f"Cliente: {c.nome} (codigo {c.codigo})")
    print("Itens:")


    for item in v.itens:
        p = service.produtos.buscar(item["codigo_produto"])
        nome = p.nome if p else "Produto removido"


        print(
            f"  {nome} (codigo {item['codigo_produto']}) | "
            f"Quantidade: {item['quantidade']} | "
            f"Preco: R$ {item['preco_unitario']:.2f} | "
            f"Subtotal: R$ "
            f"{item['quantidade'] * item['preco_unitario']:.2f}"
        )


    print(f"Total da venda: R$ {v.valor_total:.2f}")




def menu():
    print("""
==============================
     SISTEMA DE ESTOQUE
==============================
1  - Cadastrar cliente
2  - Listar clientes
3  - Buscar cliente
4  - Remover cliente
5  - Cadastrar produto
6  - Listar produtos
7  - Buscar produto
8  - Atualizar estoque
9  - Remover produto
10 - Listar produtos em ordem inversa
11 - Listar produtos ordenados por ID
12 - Buscar produto por ID usando Busca Binaria
13 - Realizar venda simples de exemplo
14 - Visualizar fila de vendas
15 - Visualizar primeira venda da fila
16 - Exibir valor total do estoque
17 - Exibir valor total das vendas
18 - Exibir clientes e valores totais gastos
19 - Exibir cliente que mais gastou
20 - Exibir produto mais vendido
21 - Desfazer ultima operacao
0  - Sair
==============================""")
