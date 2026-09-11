import os

from estruturas.fila import Fila
from estruturas.lde import LDE
from estruturas.lse import LSE
from estruturas.pilha import Pilha

from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda

from algoritmos.ordenacao import ordenar_produtos_por_id
from algoritmos.busca_binaria import buscar_produto_por_id

from services.persistencia_service import PersistenciaService


class EstoqueService:

    def __init__(self):
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.persistencia = PersistenciaService(
            os.path.join(raiz, "data")
        )

        self.clientes = LSE()
        self.produtos = LDE()
        self.vendas = Fila()
        self.historico = Pilha()

        self.carregar_dados()

    def carregar_dados(self):
        for c in self.persistencia.carregar_clientes():
            self.clientes.inserir_fim(c)

        for p in self.persistencia.carregar_produtos():
            self.produtos.inserir_fim(p)

        for v in self.persistencia.carregar_vendas():
            self.vendas.enqueue(v)

    def proximo_codigo(self, lista):
        return max((x.codigo for x in lista), default=0) + 1

    # CLIENTES

    def cadastrar_cliente(self, nome):
        c = Cliente(self.proximo_codigo(self.clientes.listar()), nome)
        self.clientes.inserir_fim(c)

        self.historico.push({
            "acao": "cadastrar_cliente",
            "cliente": c
        })

        self.salvar_clientes()
        return c

    def listar_clientes(self):
        return self.clientes.listar()

    def buscar_cliente(self, codigo):
        c = self.clientes.buscar(codigo)

        if c is None:
            raise ValueError(
                f"Cliente com codigo {codigo} nao encontrado."
            )

        return c

    def remover_cliente(self, codigo):
        c = self.clientes.remover(codigo)

        if c is None:
            raise ValueError(
                f"Cliente com codigo {codigo} nao encontrado."
            )

        self.historico.push({
            "acao": "remover_cliente",
            "cliente": c
        })

        self.salvar_clientes()
        return c

    # PRODUTOS

    def cadastrar_produto(self, nome, preco, quantidade):
        p = Produto(
            self.proximo_codigo(self.produtos.listar()),
            nome,
            preco,
            quantidade
        )

        self.produtos.inserir_fim(p)

        self.historico.push({
            "acao": "cadastrar_produto",
            "produto": p
        })

        self.salvar_produtos()
        return p

    def listar_produtos(self):
        return self.produtos.listar()

    def listar_produtos_inverso(self):
        return self.produtos.listar_inverso()

    def listar_produtos_ordenados_por_id(self):
        return ordenar_produtos_por_id(
            self.produtos.listar()
        )

    def buscar_produto(self, codigo):
        p = self.produtos.buscar(codigo)

        if p is None:
            raise ValueError(
                f"Produto com codigo {codigo} nao encontrado."
            )

        return p

    def buscar_produto_binario(self, codigo):
        produtos = ordenar_produtos_por_id(
            self.produtos.listar()
        )

        p = buscar_produto_por_id(produtos, codigo)

        if p is None:
            raise ValueError(
                f"Produto com codigo {codigo} nao encontrado."
            )

        return p

    def atualizar_estoque(self, codigo, nova_quantidade):
        p = self.buscar_produto(codigo)
        antiga = p.quantidade

        p.atualizar_estoque(nova_quantidade)

        self.historico.push({
            "acao": "atualizar_estoque",
            "codigo": codigo,
            "quantidade_antiga": antiga
        })

        self.salvar_produtos()
        return p

    def remover_produto(self, codigo):
        p = self.produtos.remover(codigo)

        if p is None:
            raise ValueError(
                f"Produto com codigo {codigo} nao encontrado."
            )

        self.historico.push({
            "acao": "remover_produto",
            "produto": p
        })

        self.salvar_produtos()
        return p

    # VENDAS

    def gerar_codigo_venda(self):
        return self.proximo_codigo(self.vendas.listar())

    def realizar_venda_exemplo(
        self,
        codigo_cliente,
        codigo_produto,
        quantidade
    ):
        cliente = self.buscar_cliente(codigo_cliente)
        produto = self.buscar_produto(codigo_produto)

        if quantidade <= 0:
            raise ValueError(
                "A quantidade vendida deve ser maior que zero."
            )

        if produto.quantidade < quantidade:
            raise ValueError(
                f"Estoque insuficiente. Estoque atual: "
                f"{produto.quantidade}."
            )

        estoque_anterior = produto.quantidade
        produto.atualizar_estoque(
            produto.quantidade - quantidade
        )

        venda = Venda(
            self.gerar_codigo_venda(),
            cliente.codigo,
            [{
                "codigo_produto": produto.codigo,
                "quantidade": quantidade,
                "preco_unitario": produto.preco
            }]
        )

        self.vendas.enqueue(venda)

        self.historico.push({
            "acao": "realizar_venda",
            "venda": venda,
            "codigo_cliente": cliente.codigo,
            "nome_cliente": cliente.nome,
            "codigo_produto": produto.codigo,
            "nome_produto": produto.nome,
            "quantidade": quantidade,
            "estoque_anterior": estoque_anterior
        })

        self.salvar_produtos()
        self.salvar_vendas()

        return venda

    def listar_vendas(self):
        return self.vendas.listar()

    def primeira_venda(self):
        return self.vendas.front()

    # RELATORIOS

    def valor_total_estoque(self):
        return sum(
            p.preco * p.quantidade
            for p in self.produtos.listar()
        )

    def valor_total_vendas(self):
        return sum(
            v.valor_total
            for v in self.vendas.listar()
        )

    def clientes_e_valores_totais_gastos(self):
        resultado = []

        for c in self.clientes.listar():
            total = sum(
                v.valor_total
                for v in self.vendas.listar()
                if v.codigo_cliente == c.codigo
            )
            resultado.append((c, total))

        return resultado

    def cliente_que_mais_gastou(self):
        dados = self.clientes_e_valores_totais_gastos()

        return max(dados, key=lambda x: x[1]) if dados else None

    def produto_mais_vendido(self):
        quantidades = {}

        for v in self.vendas.listar():
            for item in v.itens:
                codigo = item["codigo_produto"]
                quantidades[codigo] = (
                    quantidades.get(codigo, 0)
                    + item["quantidade"]
                )

        if not quantidades:
            return None

        codigo = max(quantidades, key=quantidades.get)
        produto = self.produtos.buscar(codigo)

        return (
            (produto, quantidades[codigo])
            if produto else None
        )

    # DESFAZER

    def desfazer_ultima_operacao(self):
        if self.historico.is_empty():
            raise IndexError(
                "Nao ha operacoes para desfazer."
            )

        op = self.historico.pop()
        acao = op["acao"]

        if acao == "cadastrar_cliente":
            self.clientes.remover(op["cliente"].codigo)
            self.salvar_clientes()

        elif acao == "remover_cliente":
            self.clientes.inserir_fim(op["cliente"])
            self.salvar_clientes()

        elif acao == "cadastrar_produto":
            self.produtos.remover(op["produto"].codigo)
            self.salvar_produtos()

        elif acao == "remover_produto":
            self.produtos.inserir_fim(op["produto"])
            self.salvar_produtos()

        elif acao == "atualizar_estoque":
            p = self.produtos.buscar(op["codigo"])

            if p:
                p.atualizar_estoque(
                    op["quantidade_antiga"]
                )

            self.salvar_produtos()

        elif acao == "realizar_venda":
            venda = op["venda"]

            self.vendas = Fila()

            for v in self.persistencia.carregar_vendas():
                if v.codigo != venda.codigo:
                    self.vendas.enqueue(v)

            p = self.produtos.buscar(
                op["codigo_produto"]
            )

            if p:
                p.atualizar_estoque(
                    op["estoque_anterior"]
                )

            self.salvar_produtos()
            self.salvar_vendas()

        return op

    # PERSISTENCIA

    def salvar_clientes(self):
        self.persistencia.salvar_clientes(
            self.clientes.listar()
        )

    def salvar_produtos(self):
        self.persistencia.salvar_produtos(
            self.produtos.listar()
        )

    def salvar_vendas(self):
        self.persistencia.salvar_vendas(
            self.vendas.listar()
        )