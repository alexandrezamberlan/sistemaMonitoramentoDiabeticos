# Sistema de Monitoramento de Diabetes
    Projeto desenvolvido por alunos dos cursos da Computação, em uma parceria com o Laboratório de Práticas da Computação UFN e a empresa ER Clinic.

## Registro no INPI: ????

## Versão:
    1.0 de Novembro de 2021
    1.1 de Março de 2022
    1.2 de Junho de 2022
    1.3 de Dezembro de 2025

## Apoio da Universidade Franciscana

## Colaboradores:
### UFN
    Professores:
        Alexandre Zamberlan - responsável técnico e integrante do Laboratório de Práticas da Computação
        Ana Paula Canal - coordenadora dos cursos de Computação UFN
        Elisangela Colpo - Professora do Curso de Nutrição
        Franceliane Jobim Benedetti - Professora do Curso de Nutrição
        Ricardo Frohlich da Silva - coordenador adjunto dos cursos de Computação UFN
        Sylvio André Garcia Vieira - coordenador do Laboratório de Práticas da Computação

    Alunos
        Alisson de Almeida Lamarque - Sistemas de Informação
        Camille Rodrigues - Sistemas de Informação
        Claython da Silva Ludovico - Ciência da Computação
        Eduardo Pavani Palharini - Sistemas de Informação
        Emanuel Fagan Bissacotti - Ciência da Computação
        Eric Pereira Posser - Sistemas de Informação
        Fernando Torres Moreira - Ciência da Computação
        Gabriel Braganholo - Ciência da Computação
        Gabriel Segala Soares - Ciência da Computação
        Guilherme Henriques - Ciência da Computação
        Guilherme Scher - Ciência da Computação
        Gustavo Iago Magalhães Becker - Ciência da Computação
        João Pedro Toaldo - Sistemas de Informação
        Joseph Strücker Calgaro - Sistemas de Informação
        Leonardo Barros Schroter - Sistemas de Informação
        Luiz Batista Cardoso - Ciência da Computação
        Luiz Henrique Baldissera Ghisleri - Ciência da Computação
        Matheus Filipe Nascimento de Freitas - Sistemas de Informação
        Matheus Uliana Rossato - Sistemas de Informação
        Pedro Henrique Canabarro - Ciência da Computação
        Pedro Kröning Corrêa Balen - Ciência da Computação
        Rian Beskow Friedrich - Ciência da Computação
        Robson Cezário - Sistemas de Informação
### Consultoria:
    Gedson Leal Gomes - Educador Físico e Personal Trainer
    Empresa ER Clinic - Robertson Ebling dos Santos (egresso do curso de Sistemas de Informação UFN)


# Estruturação

- apps
    - (OK)usuario
        - tipos: administrador, cliente, nutricionista educador físico, médico 
        - nome
        - email (chave primária)
        - celular
        - cpf
        - data_nascimento
        - peso ??
        - altura ??
        - relação carb_insulina
        - relação glicemina_insulina
        - is_active
        - slug
        Obs.:
            - usuário faz autocadastro (exceto administrador)
                - colocar campo de aceite dos termos de uso
                - verificar se está mandando por email a ativação do usuário
    
    - (OK)alimento
        - descrição do alimento
        - unidade do alimento
        - quantidade calorias por unidade do alimento
        - quantidade de carboidratos por unidade do alimento
        - fonte de referência
        - is_active
        - slug

    - (OK)atividade_fisica 
        - nome
        - detalhes da atividade (texto)
        - tipo da atividade
        - is_active
        - slug
        
    - (OK)medicamento
        - nome fantasia
        - nome referência
        - is_active
        - slug

## Sugestões de CSS
    - https://bootswatch.com/3/
    - Icons bootstrap 
        - https://www.w3schools.com/icons/bootstrap_icons_glyphicons.asp

## .env
```
SECRET_KEY='aoabb!bk-g5s0uk49ecc#%3#3+is(&3+)@ny%3yo0ct0481q43'

DEBUG=True

STATIC_URL=/static/

DOMINIO_URL='http://localhost:8000'
GERADORSQL_URL=''

EMAIL_HOST_USER = ''
EMAIL_BACKEND='gmailapi_backend.mail.GmailBackend'
GMAIL_API_CLIENT_ID=''
GMAIL_API_CLIENT_SECRET=''
GMAIL_API_REFRESH_TOKEN=''
EMAIL_REPLY_TO = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_USE_STARTTLS = False
GEMINI_API_KEY = ''
```
