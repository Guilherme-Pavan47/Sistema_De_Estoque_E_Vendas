# Sistema De Estoque E Vendas

Sistema desenvolvido em **Python** para gerenciamento de clientes, produtos, estoque e vendas. O projeto foi desenvolvido para aplicar conceitos de **Estrutura de Dados, algoritmos, modularização e orientação a objetos**.

## Integrantes

* **Guilherme Luiz Pavan Vial** — RA: 1139397
* **Lorenzo Pomatti** — RA: 1139572
* **Otavio Biazus De Mello** — RA: 1139244
* **Marco Antonio Pasinato** — RA: 1139597
* **Michel Balzan Da Veiga** — RA: 1139750

---

## Tecnologias utilizadas

### Python

Principal linguagem do projeto, utilizada para desenvolver toda a lógica do sistema, estruturas de dados, algoritmos, modelos e regras de negócio.

### Git e GitHub

Utilizados para controle de versões, armazenamento do código e desenvolvimento colaborativo.

### Visual Studio Code

Ambiente utilizado para desenvolvimento, edição e execução do projeto.

### Arquivos CSV

Utilizados para armazenar os dados de clientes, produtos e vendas, permitindo que as informações permaneçam salvas após o encerramento do programa.

---

## Estruturas de Dados

O projeto implementa as estruturas de dados manualmente:

* **LSE (Lista Simplesmente Encadeada):** utilizada para armazenar clientes.
* **LDE (Lista Duplamente Encadeada):** utilizada para armazenar produtos.
* **Fila:** utilizada para armazenar as vendas, seguindo o conceito **FIFO** (First In, First Out).
* **Pilha:** utilizada para armazenar operações que podem ser desfeitas, seguindo o conceito **LIFO** (Last In, First Out).

---

## Algoritmos

### Insertion Sort

Utilizado para ordenar os produtos por ID.

### Busca Binária

Utilizada para localizar produtos pelo ID de forma eficiente em uma lista ordenada.

---

## Funcionalidades

O sistema permite:

* Cadastrar, consultar e remover clientes;
* Cadastrar, consultar, atualizar e remover produtos;
* Controlar o estoque;
* Realizar vendas;
* Consultar a fila de vendas;
* Calcular valores do estoque e das vendas;
* Identificar clientes que mais gastaram;
* Identificar produtos mais vendidos;
* Ordenar produtos;
* Realizar busca binária;
* Desfazer operações;
* Salvar e carregar dados através de arquivos CSV.

---

## Organização do projeto

```text
Sistema_De_Estoque_E_Vendas/
│
├── main.py
├── models/
│   ├── cliente.py
│   ├── produto.py
│   └── venda.py
│
├── estruturas/
│   ├── nodo.py
│   ├── dnodo.py
│   ├── lse.py
│   ├── lde.py
│   ├── fila.py
│   └── pilha.py
│
├── algoritmos/
│   ├── ordenacao.py
│   └── busca_binaria.py
│
├── services/
│   ├── estoque_service.py
│   └── persistencia_service.py
│
├── data/
│   ├── clientes.csv
│   ├── produtos.csv
│   └── vendas.csv
│
└── README.md
```

### Organização das pastas

* **models:** classes de Cliente, Produto e Venda.
* **estruturas:** estruturas de dados utilizadas pelo sistema.
* **algoritmos:** algoritmos de ordenação e busca.
* **services:** regras do sistema e persistência dos dados.
* **data:** arquivos CSV utilizados para armazenamento.
* **main.py:** responsável pelo menu e execução do programa.

---

## Como executar

É necessário ter **Python 3.x** instalado.

Clone o repositório:

```bash
git clone https://github.com/Guilherme-Pavan47/Sistema_De_Estoque_E_Vendas.git
```

Entre na pasta:

```bash
cd Sistema_De_Estoque_E_Vendas
```

Execute:

```bash
python main.py
```

---

## Objetivo

O objetivo do projeto é aplicar na prática os conceitos estudados em **Estrutura de Dados**, utilizando listas encadeadas, fila, pilha, algoritmos de ordenação e busca, além de modularização, orientação a objetos e persistência de dados.
