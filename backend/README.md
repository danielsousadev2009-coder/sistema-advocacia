# Backend — Sistema de Gestão Jurídica

Etapa 1: Autenticação completa (Django + DRF + JWT via cookie httpOnly).

## 1. Setup inicial

```bash
# Criar e ativar um ambiente virtual
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Copiar e ajustar variáveis de ambiente
cp .env.example .env
```

Edite o `.env` com as credenciais do seu PostgreSQL local. Se ainda não
tem um banco criado:

```bash
psql -U postgres -c "CREATE DATABASE gestao_juridica;"
```

## 2. Migrations

```bash
python manage.py makemigrations core accounts
python manage.py migrate
```

## 3. Criar um superusuário (para acessar o /admin/ e testar login)

```bash
python manage.py createsuperuser
```

O comando vai pedir e-mail e senha (não pede "username", já que o login
é por e-mail). Ele será criado com `role=admin` automaticamente.

## 4. Rodar o servidor

```bash
python manage.py runserver
```

A API sobe em `http://localhost:8000`.

## 5. Testando os endpoints

### Login
```bash
curl -i -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com", "password": "sua-senha"}' \
  -c cookies.txt
```
Deve retornar `200 OK` com os dados do usuário no corpo, e os cookies
`access_token` e `refresh_token` salvos em `cookies.txt`.

### Dados do usuário logado
```bash
curl -i http://localhost:8000/api/auth/me/ -b cookies.txt
```
Deve retornar `200 OK` com nome, e-mail, role, etc.

### Renovar o access token
```bash
curl -i -X POST http://localhost:8000/api/auth/refresh/ -b cookies.txt -c cookies.txt
```

### Logout
```bash
curl -i -X POST http://localhost:8000/api/auth/logout/ -b cookies.txt
```
Deve retornar `204 No Content` e limpar os cookies.

### Esqueci minha senha
```bash
curl -i -X POST http://localhost:8000/api/auth/forgot-password/ \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com"}'
```
Por enquanto, o link de redefinição aparece no **console onde o
`runserver` está rodando** (ainda não enviamos e-mail de verdade — isso
fica para uma etapa futura de infraestrutura). Copie o `token` impresso
no console para o próximo passo.

### Redefinir a senha
```bash
curl -i -X POST http://localhost:8000/api/auth/reset-password/ \
  -H "Content-Type: application/json" \
  -d '{"token": "TOKEN_DO_CONSOLE", "password": "nova-senha-123"}'
```

## 6. Testando erros esperados (importante confirmar que a segurança funciona)

- Login com senha errada → deve retornar `401`, nunca `200`.
- `GET /api/auth/me/` sem estar logado (sem cookies) → deve retornar `401`.
- Reset de senha com token usado duas vezes → segunda tentativa deve
  retornar `400`.

## 7. Documentação interativa da API

Com o servidor rodando, acesse:
```
http://localhost:8000/api/schema/docs/
```
Isso já vem pronto (drf-spectacular) e será usado depois para gerar
tipos TypeScript automaticamente no frontend.

## 8. Painel administrativo

```
http://localhost:8000/admin/
```
Use o superusuário criado no passo 3. Dá para criar/editar usuários e
escritórios manualmente por aqui enquanto os módulos de gestão de
usuários e escritórios ainda não têm tela própria no frontend.

---

## O que NÃO está incluso nesta etapa (de propósito)

- Envio real de e-mail (reset de senha só loga no console por enquanto).
- Endpoint público de cadastro (`/register/`) — conforme decidido,
  contas de cliente são criadas via aprovação de solicitação de
  atendimento (módulo futuro), e contas internas (advogado/secretaria)
  são criadas pelo admin via `/admin/`.
- Qualquer coisa relacionada a Cliente, Processo, Documento, etc. — só
  a fundação de autenticação e o modelo de tenant (`Escritorio`).

Se algo der erro em qualquer passo acima, me mande a mensagem de erro
completa antes de tentar corrigir por conta própria — vamos resolver
juntos antes de avançar para a integração com o frontend.
