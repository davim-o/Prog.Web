# 📁 Documentação da Implementação — Capítulo 12: Autenticação com Redes Sociais

Este diretório (`implementacao_capitulo12_redes_sociais/`) reúne **todos os arquivos de código implementados/modificados**, o **mapeamento exato dos diretórios no projeto `LojaPSI`** e o **detalhamento técnico linha a linha do que foi alterado**, seguindo rigorosamente a lógica do **Capítulo 12 (Autenticação com Redes Sociais — Facebook e Google OAuth2)** com `social-auth-app-django`.

---

## 🗺️ 1. Mapa de Endereços dos Arquivos Modificados

> **Equivalência entre a apostila e o nosso projeto:**
> Na apostila, o projeto base chama-se `medicSearchAdmin` (configurações) e `medicSearch` (aplicação). No nosso projeto **LojaPSI**, a pasta de configurações é **`lojaAdmin`** e a aplicação principal é **`loja`**.

| # | Arquivo no Projeto (`LojaPSI`) | Cópia nesta pasta (`arquivos_modificados/`) | Equivalente no Capítulo 12 | Função na Atividade |
| :-: | :--- | :--- | :--- | :--- |
| **1** | [`requirements.txt`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/requirements.txt) | `arquivos_modificados/requirements.txt` | Seção 12.1 (pág. 236) | Inclusão da biblioteca `social-auth-app-django` |
| **2** | [`lojaAdmin/settings/settings.py`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/lojaAdmin/settings/settings.py) | `arquivos_modificados/settings.py` | Seções 12.1 e 12.3 (págs. 237, 249, 251–252, 261) | Registro do `social_django`, `context_processors`, `AUTHENTICATION_BACKENDS` e chaves OAuth2 (Facebook e Google) |
| **3** | [`loja/urls/AuthUrls.py`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/loja/urls/AuthUrls.py) | `arquivos_modificados/AuthUrls.py` | Seção 12.2 (pág. 239) | Adição da rota `path('social-auth/', include('social_django.urls', namespace="social"))` |
| **4** | [`loja/templates/auth/auth.html`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/loja/templates/auth/auth.html) | `arquivos_modificados/auth.html` | Seções 12.2 e 12.3 (págs. 240, 250, 261) | Inclusão dos botões sociais com `{% url 'social:begin' 'facebook' %}` e `{% url 'social:begin' 'google-oauth2' %}` + layout profissional |
| **5** | [`loja/templates/usuario/usuario-edit.html`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/loja/templates/usuario/usuario-edit.html) | `arquivos_modificados/usuario-edit.html` | Seção 12.3 (págs. 254 e 262) | Painel de edição de perfil exibindo vínculo OAuth (`backends.associated` e `extra_data`) |
| **6** | [`loja/templates/base.html`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/loja/templates/base.html) | `arquivos_modificados/base.html` | Seção 12.3 (pág. 262) | Inclusão do atalho **Perfil** (`/usuario/edit`) na barra de navegação superior |
| **7** | [`loja/static/css/global.css`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/loja/static/css/global.css) e [`loja/static/css/home.css`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/loja/static/css/home.css) | `arquivos_modificados/global.css` e `arquivos_modificados/home.css` | Seção 12.2 (pág. 241) | Estilização dos botões `.social-container`, `#facebook`, `#google` e card de autenticação moderno |
| **8** | [`lojaAdmin/db.sqlite3`](file:///C:/Users/20241011110031/.gemini/antigravity/scratch/LojaPSI/lojaAdmin/db.sqlite3) | *(Banco migrado na raiz)* | Seção 12.1 (págs. 238–239) | Tabelas do `social_django` criadas via `python manage.py migrate` (`social_auth_usersocialauth`, `social_auth_nonce`, `social_auth_association`, etc.) |

---

## 🔍 2. Detalhamento Passo a Passo do Que Foi Modificado

### Passo 1 — Instalação do Módulo (`requirements.txt` e Terminal)
- **Onde:** `C:\Users\20241011110031\.gemini\antigravity\scratch\LojaPSI\requirements.txt`
- **O que foi feito:**
  ```bash
  pip install social-auth-app-django
  ```
  Adicionado `social-auth-app-django` ao `requirements.txt` para gerenciar a autenticação OAuth2 com redes sociais.

---

### Passo 2 — Configuração do `settings.py`
- **Onde:** `C:\Users\20241011110031\.gemini\antigravity\scratch\LojaPSI\lojaAdmin\settings\settings.py`
- **O que foi modificado:**
  1. **`INSTALLED_APPS` (Linhas 32–42):** Adicionado `'social_django'` para registrar as tabelas e recursos de autenticação social no projeto Django:
     ```python
     INSTALLED_APPS = [
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.messages',
         'django.contrib.staticfiles',
         'loja',
         'social_django',
     ]
     ```
  2. **`TEMPLATES['OPTIONS']['context_processors']` (Linhas 62–71):** Adicionados os *context processors* que injetam `backends` e `login_redirect` automaticamente nos templates HTML:
     ```python
     'social_django.context_processors.backends',
     'social_django.context_processors.login_redirect',
     ```
  3. **`AUTHENTICATION_BACKENDS` (Linhas 147–151):** Sobrescrito o atributo de autenticação do Django para aceitar login via **Google (`GoogleOAuth2`)**, **Facebook (`FacebookOAuth2`)** e manter o login tradicional por usuário/senha (**`ModelBackend`**):
     ```python
     AUTHENTICATION_BACKENDS = [
         'social_core.backends.google.GoogleOAuth2',
         'social_core.backends.facebook.FacebookOAuth2',
         'django.contrib.auth.backends.ModelBackend',
     ]
     ```
  4. **Credenciais e Dados Extras do Facebook e Google (Linhas 153–171):**
     ```python
     # Configurações do Facebook OAuth2 (Cap. 12.3)
     SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY', 'CÓDIGO ID do Aplicativo')  # App ID
     SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET', 'Chave Secreta do Aplicativo')  # App Secret

     SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']
     SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
         'fields': 'id, name, email, picture.type(large), link'
     }
     SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
         ('name', 'name'),
         ('email', 'email'),
         ('picture', 'picture'),
         ('link', 'profile_url'),
     ]

     # Configurações do Google OAuth2 (Cap. 12.3)
     SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', 'Seu ID de cliente')
     SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', 'Sua chave secreta de cliente')
     ```

---

### Passo 3 — Migração do Banco de Dados (`migrate`)
- **Comando executado:**
  ```bash
  python manage.py migrate
  ```
- **O que foi modificado no banco (`lojaAdmin/db.sqlite3`):**
  Foram aplicadas todas as migrações do `social_django` (`0001_initial` até `0016_...`), criando as tabelas:
  - `social_auth_usersocialauth` (vincula o `User` do Django ao `provider` e `uid` da rede social, além de armazenar o JSON `extra_data`)
  - `social_auth_nonce`
  - `social_auth_association`
  - `social_auth_code`
  - `social_auth_partial`

---

### Passo 4 — Configuração das URLs (`loja/urls/AuthUrls.py`)
- **Onde:** `C:\Users\20241011110031\.gemini\antigravity\scratch\LojaPSI\loja\urls\AuthUrls.py`
- **O que foi modificado:**
  Importado `include` de `django.urls` e adicionada a rota `social-auth/` com o `namespace="social"`:
  ```python
  from django.urls import path, include
  from loja.views.AuthView import login_view, register_view, logout_view

  urlpatterns = [
      path("login/", login_view, name='login'),
      path("register/", register_view, name='register'),
      path("logout", logout_view, name='logout'),
      # Rota de autenticação por redes sociais (Cap. 12.2)
      path('social-auth/', include('social_django.urls', namespace="social")),
  ]
  ```
  Isso habilita endpoints automáticos como:
  - `/social-auth/login/facebook/` e `/social-auth/complete/facebook/`
  - `/social-auth/login/google-oauth2/` e `/social-auth/complete/google-oauth2/`

---

### Passo 5 — Botões de Redes Sociais no Formulário (`loja/templates/auth/auth.html`)
- **Onde:** `C:\Users\20241011110031\.gemini\antigravity\scratch\LojaPSI\loja\templates\auth\auth.html`
- **O que foi modificado:**
  Adicionado o divisor `"Ou"` e o container `.social-container` contendo os botões para **Facebook** (`id="facebook"`) e **Google** (`id="google"`), apontando dinamicamente para a tag `{% url 'social:begin' ... %}`:
  ```html
  <!-- Botões de Login com Redes Sociais (Capítulo 12.2 e 12.3) -->
  <p class="text-center mt-3 mb-2 auth-divider" style="display: block;"><span>Ou</span></p>
  <div class="social-container">
      <a class="btn" id="facebook" href="{% url 'social:begin' 'facebook' %}" title="Entrar com Facebook">
          <i class="fa fa-facebook-f"></i>
      </a>
      <a class="btn" id="google" href="{% url 'social:begin' 'google-oauth2' %}" title="Entrar com Google">
          <i class="fa fa-google"></i>
      </a>
  </div>
  ```

---

### Passo 6 — Exibição de Perfil e Dados Extras (`loja/templates/usuario/usuario-edit.html` e `base.html`)
- **Onde:**
  - `C:\Users\20241011110031\.gemini\antigravity\scratch\LojaPSI\loja\templates\usuario\usuario-edit.html`
  - `C:\Users\20241011110031\.gemini\antigravity\scratch\LojaPSI\loja\templates\base.html`
- **O que foi modificado:**
  - Na barra de navegação (`base.html`), foi adicionado o link **Perfil** (`/usuario/edit`) para acessar rapidamente o formulário de edição de perfil (conforme Figura 12.29 da apostila).
  - No template `usuario-edit.html`, foi adicionada a leitura de `backends.associated` e `ass.extra_data.picture.data.url` (explicado na página 254 da apostila) para exibir a foto e os dados extras quando o usuário autentica via rede social.
