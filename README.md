# Sistema de Monitoramento de Diabetes

Sistema Web Python-Django que gerencia alimentação, exercícios, medicação e insulina de pacientes diabeticos

## Registro INPI: ???

Este projeto faz parte do Laboratório de Práticas da Computação UFN e a disciplina Tecnologias Inteligentes Aplicadas à Saúde, como uma prática extensionista no ensino

## Integrantes
    - Camille Rodrigues - Sistemas de Informação
    
    - Gabriel Morais - Ciência da Computação
    - Guilherme Henriques - Ciência da Computação
    - Guilherme Scher - Ciência da Computação
    - Pedro Canabarro - Ciência da Computação

    - Professora Ana Paula Canal
    - Professor Ricardo Frohlich da Silva
    - Professor Sylvio Vieira

    - Consultor da Empresa parceira ER Clinic - Robertson Ebling dos Santos

## Estruturação

- apps
    - usuario
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
    
    - alimento
        - descrição do alimento
        - unidade do alimento
        - quantidade calorias por unidade do alimento
        - quantidade de carboidratos por unidade do alimento
        - fonte de referência
        - is_active
        - slug

    - atividade_fisica 
        - nome
        - detalhes da atividade (texto)
        - tipo da atividade
        - is_active
        - slug
        
    - medicamento
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