# Imunizow

A aplicação está disponível no [Heroku](https://imunizow.herokuapp.com/). Após um período de inatividade, o dyno do Heroku entra em stand-by, então o primeiro acesso é mais lento.

# Set-Up/Configuração

A aplicação pode ser rodada com [Docker](https://docs.docker.com/engine/install/) e [Docker Compose](https://docs.docker.com/compose/install/). O arquivo .env.example tem as diretivas que precisam ser configuradas caso deseje rodar com Docker. 

```
sudo docker-compose up --build
```

# Utilização

Já existem papéis cadastrados, caso seja necessário testar. 

Profissionais de Saúde: 

**usuario:** prof1

**usuario:** prof2

**senha:** 123

Coordenador:

**usuario:** coordenador1

**senha:** 123

Paciente:

**usuario:** paciente{1-50}

**senha:** 123
