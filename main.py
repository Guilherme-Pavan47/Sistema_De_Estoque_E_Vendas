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


def executar(op, s):


    if op == 1:
        c = s.cadastrar_cliente(input("Nome do cliente: "))
        print("\nCLIENTE CADASTRADO")
        cliente_info(c)


    elif op == 2:
        print("\nCLIENTES CADASTRADOS")
        listar_clientes(s.listar_clientes())


    elif op == 3:
        c = s.buscar_cliente(inteiro("Codigo do cliente: "))
        print("\nCLIENTE ENCONTRADO")
        cliente_info(c)


    elif op == 4:
        c = s.remover_cliente(
            inteiro("Codigo do cliente a remover: ")
        )
        print("\nCLIENTE REMOVIDO")
        cliente_info(c)
        print("O cliente foi retirado do cadastro.")


    elif op == 5:
        p = s.cadastrar_produto(
            input("Nome do produto: "),
            decimal("Preco do produto: R$ "),
            inteiro("Quantidade em estoque: ")
        )
        print("\nPRODUTO CADASTRADO")
        produto_info(p)


    elif op == 6:
        print("\nPRODUTOS CADASTRADOS")
        listar_produtos(s.listar_produtos())


    elif op == 7:
        p = s.buscar_produto(
            inteiro("Codigo do produto: ")
        )
        print("\nPRODUTO ENCONTRADO")
        produto_info(p)


    elif op == 8:
        codigo = inteiro("Codigo do produto: ")
        p = s.buscar_produto(codigo)
        antiga = p.quantidade
        nova = inteiro("Nova quantidade em estoque: ")


        p = s.atualizar_estoque(codigo, nova)


        print("\nESTOQUE ATUALIZADO")
        print(f"Produto: {p.nome}")
        print(f"Codigo: {p.codigo}")
        print(f"Estoque anterior: {antiga}")
        print(f"Estoque atual: {p.quantidade}")


        if nova > antiga:
            print(f"Quantidade adicionada: {nova - antiga}")
        elif nova < antiga:
            print(f"Quantidade retirada: {antiga - nova}")


        print(
            f"Valor atual em estoque: "
            f"R$ {p.preco * p.quantidade:.2f}"
        )


    elif op == 9:
        p = s.remover_produto(
            inteiro("Codigo do produto a remover: ")
        )


        print("\nPRODUTO REMOVIDO")
        print(f"Nome do produto: {p.nome}")
        print(f"Codigo: {p.codigo}")
        print(f"Quantidade removida: {p.quantidade}")
        print(f"Preco unitario: R$ {p.preco:.2f}")
        print(
            f"Valor que estava em estoque: "
            f"R$ {p.preco * p.quantidade:.2f}"
        )
        print("Estoque restante: 0")


    elif op == 10:
        print("\nPRODUTOS EM ORDEM INVERSA")
        listar_produtos(s.listar_produtos_inverso())


    elif op == 11:
        print("\nPRODUTOS ORDENADOS POR CODIGO")
        listar_produtos(s.listar_produtos_ordenados_por_id())


    elif op == 12:
        p = s.buscar_produto_binario(
            inteiro("Codigo do produto: ")
        )
        print("\nPRODUTO ENCONTRADO PELA BUSCA BINARIA")
        produto_info(p)


    elif op == 13:
        cliente = inteiro("Codigo do cliente: ")
        produto = inteiro("Codigo do produto: ")
        qtd = inteiro("Quantidade vendida: ")


        c = s.buscar_cliente(cliente)
        p = s.buscar_produto(produto)
        estoque_antigo = p.quantidade


        v = s.realizar_venda_exemplo(
            cliente, produto, qtd
        )


        print("\nVENDA REALIZADA")
        print(f"Codigo da venda: {v.codigo}")
        print(f"Cliente: {c.nome} (codigo {c.codigo})")
        print(f"Produto: {p.nome} (codigo {p.codigo})")
        print(f"Quantidade vendida: {qtd}")
        print(f"Preco unitario: R$ {p.preco:.2f}")
        print(f"Subtotal: R$ {qtd * p.preco:.2f}")
        print(f"Estoque antes: {estoque_antigo}")
        print(f"Estoque depois: {p.quantidade}")
        print(f"Total da venda: R$ {v.valor_total:.2f}")


    elif op == 14:
        print("\nFILA DE VENDAS")
        listar_vendas(s.listar_vendas(), s)


    elif op == 15:
        print("\nPRIMEIRA VENDA DA FILA")
        detalhes_venda(s.primeira_venda(), s)


    elif op == 16:
        produtos = s.listar_produtos()
        print("\nVALOR TOTAL DO ESTOQUE")
        print(f"Produtos cadastrados: {len(produtos)}")
        print(f"Valor total: R$ {s.valor_total_estoque():.2f}")


    elif op == 17:
        vendas = s.listar_vendas()
        print("\nVALOR TOTAL DAS VENDAS")
        print(f"Vendas registradas: {len(vendas)}")
        print(f"Valor total: R$ {s.valor_total_vendas():.2f}")


    elif op == 18:
        print("\nCLIENTES E VALORES TOTAIS GASTOS")


        for c, valor in s.clientes_e_valores_totais_gastos():
            print(
                f"Cliente: {c.nome} | Codigo: {c.codigo} | "
                f"Total gasto: R$ {valor:.2f}"
            )


    elif op == 19:
        resultado = s.cliente_que_mais_gastou()


        print("\nCLIENTE QUE MAIS GASTOU")


        if resultado is None:
            print("Nenhum cliente com compras registradas.")
        else:
            c, valor = resultado
            print(f"Nome: {c.nome}")
            print(f"Codigo: {c.codigo}")
            print(f"Total gasto: R$ {valor:.2f}")


    elif op == 20:
        resultado = s.produto_mais_vendido()


        print("\nPRODUTO MAIS VENDIDO")


        if resultado is None:
            print("Nenhuma venda registrada.")
        else:
            p, qtd = resultado


            if p:
                print(f"Nome: {p.nome}")
                print(f"Codigo: {p.codigo}")
                print(f"Estoque atual: {p.quantidade}")


            print(f"Quantidade vendida: {qtd}")


    elif op == 21:
        op = s.desfazer_ultima_operacao()


        print("\nULTIMA OPERACAO DESFEITA")


        if op["acao"] == "remover_produto":
            p = op["produto"]
            print("Acao: remocao de produto")
            print(f"Nome: {p.nome}")
            print(f"Codigo: {p.codigo}")
            print(f"Quantidade restaurada: {p.quantidade}")
            print(f"Preco: R$ {p.preco:.2f}")
            print(
                f"Valor restaurado: "
                f"R$ {p.preco * p.quantidade:.2f}"
            )
            print(f"Estoque atual: {p.quantidade}")


        elif op["acao"] == "cadastrar_produto":
            p = op["produto"]
            print("Acao: cadastro de produto")
            print(f"Nome: {p.nome}")
            print(f"Codigo: {p.codigo}")
            print(f"Quantidade retirada: {p.quantidade}")
            print("Estoque atual: 0")


        elif op["acao"] == "remover_cliente":
            c = op["cliente"]
            print("Acao: remocao de cliente")
            cliente_info(c)
            print("Cliente restaurado no cadastro.")


        elif op["acao"] == "cadastrar_cliente":
            c = op["cliente"]
            print("Acao: cadastro de cliente")
            cliente_info(c)
            print("Cliente retirado do cadastro.")


        elif op["acao"] == "atualizar_estoque":
            p = s.buscar_produto(op["codigo"])
            print("Acao: atualizacao de estoque")
            print(f"Produto: {p.nome}")
            print(f"Codigo: {p.codigo}")
            print(f"Estoque restaurado: {p.quantidade}")
            print(f"Preco: R$ {p.preco:.2f}")
            print(
                f"Valor em estoque: "
                f"R$ {p.preco * p.quantidade:.2f}"
            )


        elif op["acao"] == "realizar_venda":
            print("Acao: realizacao de venda")
            print(f"Codigo da venda: {op['venda'].codigo}")
            print(
                f"Cliente: {op['nome_cliente']} "
                f"(codigo {op['codigo_cliente']})"
            )
            print(
                f"Produto: {op['nome_produto']} "
                f"(codigo {op['codigo_produto']})"
            )
            print(
                f"Quantidade devolvida ao estoque: "
                f"{op['quantidade']}"
            )
            print(
                f"Estoque restaurado: "
                f"{op['estoque_anterior']}"
            )
            print(
                f"Valor da venda desfeita: "
                f"R$ {op['venda'].valor_total:.2f}"
            )


    else:
        print("Opcao invalida.")




def main():
    service = EstoqueService()


    while True:
        menu()


        try:
            opcao = inteiro("Escolha uma opcao: ")


            if opcao == 0:
                print("Sistema encerrado.")
                break


            executar(opcao, service)


        except (ValueError, IndexError) as erro:
            print(f"Erro: {erro}")


        except Exception as erro:
            print(f"Ocorreu um erro: {erro}")


        pausa()




if __name__ == "__main__":
    main()
