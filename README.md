# Best Route App
 
# Intro
 
O projeto BestRouteApp oferece uma interface CLI (Command Line Interface) e uma API (Application Program Interface) para a consultar as rotas de melhor custo entre duas localidades considerando as conexões entre todas as localidades disponíveis, mais conhecido em banco de dados de grafos como "shortest path".

Esse projeto utiliza o algoritmo de "shortest path" criado pelo cientista da computação holandês Edsger Dijkstra em 1956, e amplamente usado em softwares de logística e banco de dados de grafos.

# Arquitetura

A linguagem de desenvolvimento utilizada foi Python por ser uma linguagem madura e muito utilizada em algoritmos matemáticos e de machine learning, além de fornecer a possibilidade de criação de aplicações em linha de comando, bem como APIs do tipo REST por meio de frameworks como o Flask, utilizado nesse projeto.

O armazenamento das rotas com os seus custos foi feito em arquivo .csv, mas facilmente portado para um banco de dados relacional, não-relacional ou idealmente um banco de dados de grafo.

Essa portabilidade se dá devido a criação de uma classe "Controllers" que oferece os métodos necessários de CRUD (create, read, update, delete) para as rotas, bem o método que realiza o cálculo e retorna a rota com menor custo entre dois pontos (shortest path).

Uma classe chamada "GraphBase" é responsável pela manipulação do arquivo .csv, e juntamente com os "controllers", oferece de forma básica um banco de dados de grafo com a funcionalidade "shortest path" via API REST.

A classe de "GraphBase" também é compartilhada com a interface CLI, expondo o método de "shortest path" diretamente para essa interface.

Os testes unitários são executados via pytest, um módulo próprio do python para esse fim, e executa consultas diretamente na base de dados (arquivo csv) e também via http na API REST.

Conteúdo do projeto:
api.py - Aplicação responsável por executar o servidor rest no servidor localhost, porta 3000.

cli.py - Aplicação responsável por executar a interface de linha de comando.

test.py - Executa os testes unitários.

database.ini - Local onde está localizado o arquivo csv (base de dados com as rotas).

controllers.py - Controllers (métodos) usados nas requisições via API REST para acessar a base de dados com as rotas.

model.py - Interface entre a aplicação CLI (cli.py) e a API (api.py) e os dados, executa operações de CRUD e o "shortest path".

data\routesdb.csv - Arquivo csv com as rotas mantidas via CRUD.

data\input-routes-test.csv - Arquivo válido destinado a teste unitário.

data\input-routes-test-invalid.csv - Arquivo inválido destinado a teste unitário.

log\bestroute.log - Arquivo com mensagens de logs.

requirements.txt - Arquivo com as dependências do projeto.

input-routes.csv - Arquivo para teste da interface CLI.

bestroute_postman.json - Uma collection para executar os endepoints no app Postman.


# Instalação:

O projeto foi desenvolvido com a versão 3.8.5, mas como não usa nenhum módulo específico não deve ter problema com versões mais antigas.
Será também necessário o utilitário pip para instalar dependências.

Instalar as dependências do Python

pip install -r requirements.txt

# Testes:

Executar o servidor da API:

python api.py

pytest -v test.py

# Execução:

Para interface CLI:

Informando um arquivo csv válido, por exemplo:

python cli.py arquivo.csv 

Entrar com rotas no format OOO-DDD, por exemplo, GRU-CDG

Para ajuda:

python cli.py help 

Para API REST (usar a collection no Postman para testes)

python api.py




