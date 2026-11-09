# BIOZON Purificadores

Há alguns meses, meu tio me procurou comentando sobre a dificuldade de adaptar a sua empresa de purificadores de água aos novos tempos. Ele já acumula mais de 30 anos de serviço no mercado, com uma base fiel de clientes em Fortaleza, mas mantinha todo o controle operacional em papéis e agendas físicas.

A ideia inicial era criar algo simples e visual para a internet. Durante o processo, refiz e modifiquei o projeto diversas vezes: entender a fundo os requisitos de um negócio tradicional e a rotina da clientela dele exigiu bastante estudo e adaptação.

Buscando transmitir a essência de água pura e saúde de forma marcante, desenvolvi um visual fluido com vídeos integrados ao fundo da aplicação. A navegação traz essa sensação de leveza e clareza logo no primeiro contato.

Porém, observando a rotina do negócio, percebi um detalhe fundamental: o maior retorno financeiro da empresa não está na venda isolada dos purificadores, mas sim no ciclo recorrente de manutenção preventiva e troca periódica dos refis.

Para resolver essa dor, construí um sistema completo em Python. A aplicação conta com um portal público e um painel de gestão administrativa integrado a um banco de dados SQL, permitindo registrar clientes, controlar datas de manutenção e gerar comprovantes e ordens de serviço.

Pensei em manter o repositório privado, mas o resultado final refletiu exatamente o equilíbrio entre necessidade de negócio e solução técnica. Como estou em busca da minha inserção no mercado de desenvolvimento de software, disponibilizo este projeto como demonstração prática da minha evolução.

---

## Demonstração do Sistema

<!-- SEU VIDEO AQUI:


 Arraste seu arquivo .mp4 para esta linha no editor do GitHub -->




https://github.com/user-attachments/assets/4dc4fdd5-2ba7-4c1c-b004-f55940847c01


---

## Estrutura Técnica e Arquitetura

* Backend: Python com FastAPI e Uvicorn
* Templates e Renderização: Jinja2 com HTML5 e CSS3 responsivo
* Banco de Dados: SQLAlchemy e SQLite (pronto para migração PostgreSQL)
* Autenticação e Segurança: Rotas protegidas para gestão administrativa
* Servidor Web e Proxy: Nginx com suporte a mídias estáticas e SSL
* Sistema Operacional: Linux (Ubuntu) com gerenciamento de serviço via Systemd

---

## Funcionalidades Principais

* Interface pública focada na conversão de leads e apresentação da marca
* Catálogo interativo de produtos com especificações técnicas e suporte a falhas de mídia
* Assistente de decisão para recomendação do purificador ideal
* Canal direto de atendimento e conformidade com a LGPD
* Painel restrito para controle de clientes, chamados técnicos e agenda de trocas de refil
