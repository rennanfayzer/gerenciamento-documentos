# 📄 Sistema de Gerenciamento de Documentos

![Django](https://img.shields.io/badge/Django-5.2.7-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16.0-ff1709?style=for-the-badge&logo=django&logoColor=white)

Sistema completo para gestão de documentos de funcionários com controle de acesso, autenticação, logs de atividades, geração de relatórios em PDF e interface responsiva.

---

## 📋 Índice

- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
  - [Desenvolvimento Local](#desenvolvimento-local)
  - [Produção com Docker](#produção-com-docker)
  - [Produção no Windows (Waitress)](#produção-no-windows-waitress)
- [Configuração](#-configuração)
- [Segurança](#-segurança)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API REST](#-api-rest)
- [Comandos Úteis](#-comandos-úteis)
- [Deploy](#-deploy)
- [Testes](#-testes)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## ✨ Características

### 🔐 Autenticação e Autorização
- Sistema de login com autenticação Django
- Controle de permissões por perfil (Admin, Gestor, Funcionário)
- Autenticação via Token (DRF TokenAuthentication)
- Proteção CSRF e segurança aprimorada

### 📁 Gestão de Documentos
- Upload e armazenamento de documentos
- Categorização por tipo de documento
- Busca avançada com filtros
- Associação de documentos a funcionários e locais
- Versionamento e histórico de alterações

### 👥 Gestão de Funcionários
- Cadastro completo de funcionários
- Associação com locais de mobilização
- Visualização detalhada de perfil
- Listagem com filtros e paginação

### 📊 Dashboard e Relatórios
- Dashboard com métricas e gráficos (Chart.js)
- Exportação de dados para CSV/Excel (openpyxl, pandas)
- Geração de PDFs personalizados (ReportLab, WeasyPrint)
- Logs de atividades do sistema

### 🎨 Interface
- Design responsivo e moderno
- Tema claro/escuro
- Componentes reutilizáveis
- Feedback visual (toasts, spinners, skeleton loaders)

### 🔔 Notificações
- Sistema de alertas e notificações
- Notificações em tempo real

---

## 🛠️ Tecnologias

### Backend
- **Django 5.2.7** - Framework web Python
- **Django REST Framework 3.16.0** - API RESTful
- **PostgreSQL 17** - Banco de dados relacional
- **Gunicorn** - Servidor WSGI para produção
- **Waitress** - Servidor WSGI para Windows
- **WhiteNoise** - Servir arquivos estáticos

### Frontend
- **HTML5, CSS3, JavaScript**
- **Chart.js** - Gráficos interativos
- **Bootstrap 4** (via crispy-forms)
- **Django Templates** - Sistema de templates

### DevOps & Ferramentas
- **Docker & Docker Compose** - Containerização
- **Nginx** - Reverse proxy e servidor web
- **Git** - Controle de versão

### Bibliotecas Python
```
Django==5.2.7
djangorestframework==3.16.0
psycopg2-binary==2.9.9
gunicorn
whitenoise
django-widget-tweaks==1.5.0
django-chartjs==2.3.0
django-crispy-forms==2.4
django-filter==25.1
pandas==2.3.0
openpyxl==3.1.5
reportlab==4.4.1
weasyprint==65.1
pillow==11.2.1
pyotp==2.9.0
qrcode==8.2
```

---

## 📦 Pré-requisitos

### Para Desenvolvimento Local (Windows)
- Python 3.10+
- PostgreSQL 12+
- Git
- Virtualenv ou venv

### Para Produção com Docker
- Docker 20.10+
- Docker Compose 2.0+
- Git

---

## 🚀 Instalação

### Desenvolvimento Local

#### 1. Clone o repositório
```bash
git clone https://github.com/GrupoFranzen/gerenciamento-documentos.git
cd gerenciamento-documentos
```

#### 2. Crie e ative um ambiente virtual
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows CMD
python -m venv venv
venv\Scripts\activate.bat
```

#### 3. Instale as dependências
```powershell
cd documentos
pip install -r requirements.txt
```

#### 4. Configure as variáveis de ambiente
Copie o template `.env.example` para `.env` na pasta `documentos/` e ajuste os valores:

```bash
cp ../.env.example .env
```

Abra o arquivo `.env` e defina uma `SECRET_KEY` forte, além das credenciais do PostgreSQL que você criou no passo seguinte.

#### 5. Configure o banco de dados PostgreSQL
```sql
-- Execute no PostgreSQL
CREATE DATABASE doc_bd;
CREATE USER seu_usuario WITH PASSWORD 'sua_senha_segura';
ALTER ROLE seu_usuario SET client_encoding TO 'utf8';
ALTER ROLE seu_usuario SET default_transaction_isolation TO 'read committed';
ALTER ROLE seu_usuario SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE doc_bd TO seu_usuario;
```

#### 6. Execute as migrações
```powershell
python manage.py migrate
```

#### 7. Crie um superusuário
```powershell
python manage.py createsuperuser
```

#### 8. Colete os arquivos estáticos
```powershell
python manage.py collectstatic --noinput
```

#### 9. Inicie o servidor de desenvolvimento
```powershell
python manage.py runserver
```

Acesse: **http://localhost:8000**

---

### Produção com Docker

#### 1. Clone o repositório
```bash
git clone https://github.com/GrupoFranzen/gerenciamento-documentos.git
cd gerenciamento-documentos
```

#### 2. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto (ou copie o `.env.example`) com as variáveis necessárias:

```env
SECRET_KEY=prod-sua-chave-secreta-super-segura
DEBUG=0
ALLOWED_HOSTS=seu-dominio.com,45.140.193.93
DB_NAME=doc_bd
DB_USER=seu_usuario
DB_PASSWORD=sua_senha_super_segura
DB_HOST=db
DB_PORT=5432
```

#### 3. Ajuste o Nginx
Edite `nginx.conf` e altere o `server_name`:

```nginx
server_name seu-dominio.com;
```

#### 4. Build e execute os containers
```bash
docker-compose up -d --build
```

> ℹ️ O serviço do PostgreSQL não expõe a porta 5432 para fora da rede interna dos containers. Para desenvolvimento local, crie um `docker-compose.override.yml` com o mapeamento de porta desejado.

#### 5. Execute as migrações no container
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Acesse: **http://seu-dominio.com**

---

### Produção no Windows (Waitress)

#### 1. Siga os passos 1-8 da instalação local

#### 2. Instale o Waitress
```powershell
pip install waitress
```

#### 3. Configure o ambiente de produção
No arquivo `.env` ou nas variáveis de ambiente:
```env
DEBUG=0
ALLOWED_HOSTS=seu-ip-ou-dominio,localhost
```

#### 4. Execute o servidor com Waitress
Utilize o script `iniciar_servidor NOVO.bat` ou execute manualmente:

```powershell
# Ajuste os caminhos no script
.\iniciar_servidor_NOVO.bat
```

Ou diretamente:
```powershell
python -c "from waitress import serve; from documentos.wsgi import application; serve(application, host='0.0.0.0', port=5000, threads=50)"
```

Acesse: **http://localhost:5000**

---

## ⚙️ Configuração

### Configurações Importantes

#### `documentos/settings.py`

**Debug Mode**
```python
DEBUG = os.environ.get('DEBUG', '0') == '1'
```

**Banco de Dados**
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('DB_NAME', 'doc_bd'),
        "USER": os.environ.get('DB_USER', 'postgres'),
        "PASSWORD": os.environ.get('DB_PASSWORD', ''),
        "HOST": os.environ.get('DB_HOST', 'localhost'),
        "PORT": os.environ.get('DB_PORT', '5432'),
    }
}
```

**Arquivos Estáticos**
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'gestao_docs' / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Arquivos de Mídia**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 🔒 Segurança

#### 1. **Arquivo `.env` para Desenvolvimento**

Copie o `.env.example` para `.env` na raiz do projeto `documentos/` (este arquivo está no .gitignore) e ajuste os valores conforme o seu ambiente.

#### 2. **Gerar SECRET_KEY Segura**

```python
# Execute no shell Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Ou via terminal:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 3. **Configurar Produção**

Em produção (`DEBUG=0`), certifique-se de:

- ✅ Usar SECRET_KEY única e forte (mínimo 50 caracteres)
- ✅ Configurar ALLOWED_HOSTS corretamente
- ✅ Usar HTTPS (SSL/TLS)
- ✅ Configurar SECURE_SSL_REDIRECT
- ✅ Usar variáveis de ambiente do servidor/container

```python
# settings.py para produção
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

#### 4. **Proteção de Arquivos Sensíveis**

O arquivo `.gitignore` já está configurado para proteger:

- Arquivos `.env` e variações
- Backups de banco de dados (`.sql`, `.backup`)
- Arquivos de mídia (uploads de usuários)
- Tokens e credenciais (`.pem`, `.key`, etc.)
- Logs que podem conter informações sensíveis

#### 5. **Revisar Antes de Commit**

```bash
# Verifique o que será commitado
git status

# Verifique o conteúdo dos arquivos
git diff

```

#### 6. **Arquivo `.env.example`**

O repositório já inclui um `.env.example` como template. Copie-o e ajuste conforme necessário:

```bash
cp .env.example .env
```

### 🛡️ Checklist de Segurança

Antes de fazer deploy:

- [ ] SECRET_KEY é única e não está hardcoded
- [ ] DEBUG=False em produção
- [ ] ALLOWED_HOSTS configurado corretamente
- [ ] Credenciais de BD não estão no código
- [ ] Arquivos .env não estão no repositório
- [ ] HTTPS está configurado
- [ ] Cookies de sessão são seguros
- [ ] Firewall configurado (apenas portas necessárias)
- [ ] Backups automáticos configurados
- [ ] Logs de acesso monitorados
- [ ] Dependências atualizadas (sem vulnerabilidades)

### 🔍 Auditoria de Segurança

```powershell
# Verificar se há arquivos .env versionados
git log --all --full-history -- "*.env"

# Verificar vulnerabilidades em dependências
pip install safety
safety check

# Verificar configurações de segurança Django
python manage.py check --deploy
```

---

## 📂 Estrutura do Projeto

```
gerenciamento-documentos/
├── docker-compose.yml          # Orquestração Docker
├── Dockerfile                  # Imagem Docker do Django
├── nginx.conf                  # Configuração Nginx
├── README.md                   # Este arquivo
├── iniciar_servidor.bat        # Script de inicialização Windows (Waitress)
├── iniciar_servidor NOVO.bat   # Script otimizado Windows
└── documentos/                 # Projeto Django principal
    ├── manage.py               # CLI Django
    ├── requirements.txt        # Dependências Python
    ├── list_static.py          # Ferramenta para detectar duplicatas estáticas
    ├── usuarios.csv            # CSV de importação de usuários
    ├── local_mobilizacao.csv   # CSV de importação de locais
    ├── documentos/             # Configurações do projeto
    │   ├── __init__.py
    │   ├── settings.py         # Configurações principais
    │   ├── urls.py             # URLs principais
    │   ├── wsgi.py             # Entry point WSGI
    │   └── asgi.py             # Entry point ASGI
    ├── gestao_docs/            # App principal
    │   ├── models.py           # Modelos de dados
    │   ├── views.py            # Views e lógica de negócio
    │   ├── urls.py             # Rotas do app
    │   ├── forms.py            # Formulários Django
    │   ├── admin.py            # Configuração Django Admin
    │   ├── api.py              # Viewsets da API REST
    │   ├── serializers.py      # Serializadores DRF
    │   ├── permissions.py      # Permissões customizadas
    │   ├── decorators.py       # Decoradores de permissão
    │   ├── auth_utils.py       # Utilitários de autenticação
    │   ├── cache_utils.py      # Utilitários de cache
    │   ├── backup_utils.py     # Utilitários de backup
    │   ├── export_utils.py     # Exportação de dados
    │   ├── log_utils.py        # Sistema de logs
    │   ├── notifications.py    # Sistema de notificações
    │   ├── tasks.py            # Tarefas assíncronas
    │   ├── management/         # Comandos personalizados
    │   │   └── commands/
    │   │       ├── importar_csv.py       # Importar dados CSV
    │   │       └── associar_funcionarios.py
    │   ├── migrations/         # Migrações do banco
    │   ├── static/             # Arquivos estáticos (CSS, JS, imagens)
    │   │   ├── css/
    │   │   │   ├── dark-theme.css
    │   │   │   └── responsive.css
    │   │   ├── js/
    │   │   │   ├── dashboard.js
    │   │   │   ├── shortcuts.js
    │   │   │   └── theme.js
    │   │   └── img/
    │   │       ├── logo.png
    │   │       ├── logo_dark.png
    │   │       └── favicon.ico
    │   └── templates/          # Templates HTML
    │       ├── base.html
    │       ├── dashboard.html
    │       ├── login.html
    │       ├── funcionario_list.html
    │       ├── funcionario_detail.html
    │       ├── funcionario_form.html
    │       ├── documento_form.html
    │       ├── logs.html
    │       └── registration/
    └── staticfiles/            # Arquivos coletados (collectstatic)
```

---

## 🔌 API REST

A aplicação possui uma API RESTful construída com Django REST Framework.

### Autenticação

**Obter Token**
```http
POST /api/api-token-auth/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Resposta**
```json
{
  "token": "seu_token_de_autenticacao_gerado"
}
```

### Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/funcionarios/` | Lista todos os funcionários |
| POST | `/api/funcionarios/` | Cria um novo funcionário |
| GET | `/api/funcionarios/{id}/` | Detalhes de um funcionário |
| PUT | `/api/funcionarios/{id}/` | Atualiza um funcionário |
| DELETE | `/api/funcionarios/{id}/` | Remove um funcionário |
| GET | `/api/documentos/` | Lista todos os documentos |
| POST | `/api/documentos/` | Upload de documento |
| GET | `/api/locais/` | Lista locais de mobilização |
| GET | `/api/gestores/` | Lista gestores |

### Exemplo de Requisição

```bash
# Listar funcionários (com autenticação)
curl -H "Authorization: Token seu_token_aqui" \
     http://localhost:8000/api/funcionarios/
```

---

## 💻 Comandos Úteis

### Django Management

```powershell
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Iniciar servidor de desenvolvimento
python manage.py runserver

# Shell interativo do Django
python manage.py shell

# Verificar problemas no projeto
python manage.py check
```

### Comandos Personalizados

```powershell
# Importar funcionários de CSV
python manage.py importar_csv usuarios.csv

# Associar funcionários a locais
python manage.py associar_funcionarios
```

### Docker

```bash
# Build e iniciar containers
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Executar comando no container web
docker-compose exec web python manage.py migrate

# Acessar shell do container
docker-compose exec web bash

# Rebuild específico
docker-compose up -d --build web
```

### Utilitários

```powershell
# Detectar arquivos estáticos duplicados
python list_static.py

# Ou use o script batch
.\run_list_static.bat
```

---

## 🌐 Deploy

### Deploy em Produção (Linux/Docker)

1. **Configure o servidor:**
   - Instale Docker e Docker Compose
   - Configure firewall (libere portas 80, 443)
   - Configure domínio (DNS apontando para o IP)

2. **Clone e configure:**
```bash
git clone https://github.com/GrupoFranzen/gerenciamento-documentos.git
cd gerenciamento-documentos
# Edite docker-compose.yml e nginx.conf
```

3. **Inicie os serviços:**
```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

4. **Configure SSL (opcional, recomendado):**
```bash
# Usando Let's Encrypt/Certbot
sudo certbot --nginx -d seu-dominio.com
```

### Deploy no Railway/Render

1. Crie arquivo `railway.toml` ou configure via dashboard
2. Configure variáveis de ambiente
3. Conecte ao repositório Git
4. Deploy automático a cada push

### Backup do Banco de Dados

```bash
# Backup
docker-compose exec db pg_dump -U seu_usuario doc_bd > backup_$(date +%Y%m%d).sql

# Restore
cat backup_20250120.sql | docker-compose exec -T db psql -U seu_usuario doc_bd
```

---

## 🧪 Testes

```powershell
# Executar todos os testes
python manage.py test

# Executar testes de um app específico
python manage.py test gestao_docs

# Executar teste específico
python manage.py test gestao_docs.tests.TestDocumentoModel

# Com cobertura (instale coverage)
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML
```

---

## Alterações

Adições Siga estas etapas:

1. **Fork o projeto**
2. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/minha-feature
   ```
3. **Commit suas mudanças**
   ```bash
   git commit -m 'Adiciona minha feature'
   ```
4. **Push para a branch**
   ```bash
   git push origin feature/minha-feature
   ```
5. **Abra um Pull Request**

### Padrões de Código
- Siga a PEP 8 para código Python
- Documente funções e classes
- Escreva testes para novas features
- Mantenha commits atômicos e descritivos

---

## 📄 Licença

Este projeto é de propiedade do Grupo Franzen

---

## 👥 Equipe

**Desenvolvido por:** Grupo Franzen - Rennan Miranda

**Contato:** [GitHub](https://github.com/GrupoFranzen)

---

## 📝 Notas de Versão

### v1.0.0 (2025-01-20)
- ✨ Sistema completo de gestão de documentos
- 🔐 Autenticação e autorização por perfis
- 📊 Dashboard com gráficos
- 📁 Upload e gerenciamento de arquivos
- 🔌 API REST completa
- 🐳 Suporte Docker
- 🪟 Scripts para Windows (Waitress)
- 📄 Geração de PDFs e exportação de dados

---

## 🆘 Troubleshooting

### Problema: Erro ao coletar estáticos
```powershell
# Verifique permissões da pasta staticfiles
# Execute o script de diagnóstico
python list_static.py
```

### Problema: Erro de conexão com PostgreSQL
```powershell
# Verifique se o PostgreSQL está rodando
# Windows: services.msc → PostgreSQL
# Docker: docker-compose ps
```

### Problema: WhiteNoise não serve arquivos
```python
# Certifique-se que o middleware está correto em settings.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Logo após SecurityMiddleware
    # ...
]
```

### Problema: Porta 5000 ou 8000 já em uso
```powershell
# Windows - encontrar processo usando a porta
netstat -ano | findstr :5000
# Matar processo
taskkill /PID <PID> /F
```

---

**⭐ Fim**
