<div align="center">
    <h1>Netflix Web Application</h1>
</div>

<p align="center" width="100%">
    <img src="./Web-Application/static/assets/Netflix.gif" width="15%" height="10%" />
</p>

## Descrição
**Aplicação Web** para o acesso a dados dos Shows da Netflix a partir de uma Base de Dados

## Diretórios

### [Data-Preparation](/Data-Preparation/)
No Diretório `Data-Preparation` encontram-se tanto o Dataset utilizado ( [**netflix_titles.csv**](/Data-Preparation/netflix_titles.csv) ) bem como o script ( [**Netflix DataSet - Data Preparation**](/Data-Preparation/Netflix%20DataSet%20-%20Data%20Preparation.ipynb) ) utilizado para a criação da Base de Dados.

Mais ainda, este apresenta um outro diretório ( [Output_Tables](/Data-Preparation/Output_Tables/) ) onde se encontram as várias tabelas ( já povoadas ) do modelo relacional  guardadas em **formato .csv**

### [Web-Application](/Web-Application/)
No Diretório `Web-Application` encontram-se os vários ficheiros responsáveis pela execução da Aplicação que, juntamente com a Base de Dados ( **Netflix.db** ) e os vários templates utilizados ( Presentes em [**templates**](/Web-Application/templates/) ) que irão integrar a Aplicação Web.

## Dependências
### Python3 e pip 

Deve utilizar o Python 3 e o gestor de pacotes pip. Estes podem ser
instalados [em Ubuntu] através:

```
sudo apt-get install python3 python3-pip
```

### Bibliotecas Python

De forma a executar a aplicação deve certificar-se que tem instalado as bibliotecas necessárias. Para tal basta executar o comando:

```
pip install -r requirements.txt
```

## Execução

Inicie a aplicação executando `python3 server.py` e interaja com a mesma
abrindo uma janela no seu browser  com o endereço [__http://127.0.0.1:9001/__](http://127.0.0.1:9001/) 

##  Referências

- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Jinja templates](https://jinja.palletsprojects.com/en/3.0.x/)

## Autores:
- [Gonçalo Martins Esteves](https://github.com/EstevesX10), DCC/FCUP
- [Nuno Gomes](https://github.com/NightF0x26), DCC/FCUP

