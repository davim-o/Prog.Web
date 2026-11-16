# 🎨 Instruções e Prompts para o Canva IA — Apresentação dos Slides (Capítulo 12)

Este arquivo contém:
1. **Prompt Mestre (Pronto para colar no Canva IA / Design Mágico)** para gerar a apresentação automaticamente.
2. **Estrutura Slide a Slide (Conteúdo + Código + Prints a mostrar + Fala do Apresentador)** para garantir nota máxima na apresentação ao professor.

---

## 🚀 1. Prompt Único para o Canva IA (Magic Design / Criar Apresentação)

> **Como usar no Canva:**
> 1. Abra o Canva e clique em **Apresentações** -> **Design Mágico (Canva IA)**.
> 2. Cole o prompt abaixo (ou use o recurso **"Gerar texto/slides com IA"**):

```text
Crie uma apresentação acadêmica e técnica moderna em Português sobre "Implementação de Autenticação com Redes Sociais (OAuth2) no Django com social-auth-app-django - Projeto LojaPSI (Capítulo 12)". Use um design limpo, tecnológico, nas cores azul-marinho, azul-royal e branco. Estruture em 9 slides:
Slide 1: Capa - Autenticação com Redes Sociais no Django (Facebook e Google OAuth2) aplicada ao sistema LojaPSI.
Slide 2: Objetivo da Atividade - Permitir cadastro e login via Facebook e Google sem obrigar preenchimento manual, utilizando o módulo social-auth-app-django.
Slide 3: Etapa 12.1 (Instalação e Settings) - Instalação com pip install social-auth-app-django, adição de 'social_django' no INSTALLED_APPS e configuração do AUTHENTICATION_BACKENDS (GoogleOAuth2, FacebookOAuth2 e ModelBackend).
Slide 4: Migração do Banco de Dados - Execução de python manage.py migrate e criação das tabelas do social_django (User social auths, Nonces, Associations) integradas à tabela User do Django.
Slide 5: Etapa 12.2 (Configuração de URLs e Template) - Adição da rota path('social-auth/', include('social_django.urls', namespace='social')) em loja/urls/AuthUrls.py e inclusão dos botões Facebook e Google em loja/templates/auth/auth.html.
Slide 6: Etapa 12.3 (Integração Facebook OAuth2 e Extra Data) - Configuração no Facebook for Developers (App ID e App Secret), context_processors no settings.py e captura de dados extras (SOCIAL_AUTH_FACEBOOK_SCOPE e EXTRA_DATA: id, name, email, picture, link).
Slide 7: Etapa 12.3 (Integração Google OAuth2) - Configuração no Google Cloud Console (Tela de consentimento OAuth, URI de redirecionamento http://localhost:8000/social-auth/complete/google-oauth2/) e chaves SOCIAL_AUTH_GOOGLE_OAUTH2_KEY e SECRET.
Slide 8: Demonstração do Sistema LojaPSI - Telas de Login, Registro, Painel Admin (Python Social Auth) e Edição de Perfil com conta vinculada.
Slide 9: Conclusão e Benefícios - Segurança OAuth 2.0, melhor experiência do usuário (UX) e escalabilidade para múltiplas redes sociais.
```

---

## 📊 2. Conteúdo Completo Slide a Slide (Para Colar nos Slides e Apresentar)

### 🖥️ Slide 1 — Capa
- **Título:** Autenticação com Redes Sociais no Django (Capítulo 12)
- **Subtítulo:** Implementação de Login com Facebook e Google OAuth 2.0 no Sistema **LojaPSI**
- **Tecnologias:** Python • Django 4.2 • `social-auth-app-django` • OAuth 2.0
- **🎤 O que falar para o professor:**
  > *"Olá professor e colegas, nesta apresentação vamos demonstrar a implementação do Capítulo 12 no nosso projeto LojaPSI, adicionando autenticação via Facebook e Google OAuth 2.0 utilizando a biblioteca `social-auth-app-django`."*

---

### 🎯 Slide 2 — Objetivo e Arquitetura da Solução
- **Tópicos do Slide:**
  - **Problema:** O cadastro convencional exige preenchimento manual e validação de vários campos, gerando atrito para o usuário.
  - **Solução:** Autenticação federada via protocolo **OAuth 2.0** (Facebook e Google) mantendo também o login tradicional (`ModelBackend`).
  - **Mapeamento no Projeto:**
    - Apostila: `medicSearchAdmin` / `medicSearch`
    - Nosso Projeto: **`lojaAdmin`** (configurações) / **`loja`** (aplicação principal)
- **🎤 O que falar para o professor:**
  > *"Adaptamos toda a arquitetura do Capítulo 12 para a estrutura do nosso projeto LojaPSI, onde o pacote de configurações é o `lojaAdmin` e o app principal é o `loja`, mantendo o login tradicional por usuário e senha lado a lado com o login social."*

---

### ⚙️ Slide 3 — Etapa 12.1: Instalação e `settings.py`
- **Arquivo modificado:** `lojaAdmin/settings/settings.py` e `requirements.txt`
- **Código para colocar no Slide:**
  ```bash
  pip install social-auth-app-django
  ```
  ```python
  # lojaAdmin/settings/settings.py
  INSTALLED_APPS = [
      # ... apps padrão do Django
      'loja',
      'social_django',  # Módulo de autenticação social
  ]

  AUTHENTICATION_BACKENDS = [
      'social_core.backends.google.GoogleOAuth2',
      'social_core.backends.facebook.FacebookOAuth2',
      'django.contrib.auth.backends.ModelBackend',
  ]
  ```
- **🎤 O que falar para o professor:**
  > *"Na seção 12.1 instalamos o `social-auth-app-django`, injetamos o `'social_django'` no `INSTALLED_APPS` e sobrescrevemos o `AUTHENTICATION_BACKENDS` para suportar três motores de autenticação: GoogleOAuth2, FacebookOAuth2 e o ModelBackend nativo do Django."*

---

### 🗄️ Slide 4 — Etapa 12.1: Migrações e Tabelas Criadas (`migrate`)
- **Comando executado:**
  ```bash
  python manage.py migrate
  ```
- **Tópicos do Slide:**
  - Cria automaticamente as tabelas de controle do `social_django` no `db.sqlite3`:
    - `social_auth_usersocialauth` (relaciona o `User` do Django com o `provider`, `uid` e `extra_data`)
    - `social_auth_association` e `social_auth_nonce`
  - **Vantagem:** Gerencia os tokens e vínculos OAuth sem interferir na tabela `auth_user` nem no model `Usuario` da `loja`.
- **📸 Print sugerido no slide:** Print do painel `/admin/` mostrando a seção **PYTHON SOCIAL AUTH -> User social auths**.

---

### 🔗 Slide 5 — Etapa 12.2: Configuração das URLs e Botões no Formulário
- **Arquivos modificados:**
  1. `loja/urls/AuthUrls.py`
  2. `loja/templates/auth/auth.html`
- **Código para colocar no Slide:**
  ```python
  # loja/urls/AuthUrls.py
  from django.urls import path, include
  from loja.views.AuthView import login_view, register_view, logout_view

  urlpatterns = [
      path("login/", login_view, name='login'),
      path("register/", register_view, name='register'),
      path("logout", logout_view, name='logout'),
      path('social-auth/', include('social_django.urls', namespace="social")),
  ]
  ```
  ```html
  <!-- loja/templates/auth/auth.html -->
  <p class="text-center mt-3 mb-2 auth-divider" style="display: block;"><span>Ou</span></p>
  <div class="social-container">
      <a class="btn" id="facebook" href="{% url 'social:begin' 'facebook' %}">
          <i class="fa fa-facebook-f"></i>
      </a>
      <a class="btn" id="google" href="{% url 'social:begin' 'google-oauth2' %}">
          <i class="fa fa-google"></i>
      </a>
  </div>
  ```
- **📸 Print sugerido no slide:** Print da tela `/login/` e `/register/` do sistema `LojaPSI` com os botões estilizados do Facebook e Google.

---

### 📘 Slide 6 — Etapa 12.3: Configuração do Facebook e Dados Extras (`EXTRA_DATA`)
- **Arquivo modificado:** `lojaAdmin/settings/settings.py`
- **Código para colocar no Slide:**
  ```python
  # Context Processors em TEMPLATES:
  'social_django.context_processors.backends',
  'social_django.context_processors.login_redirect',

  # Chaves e Escopo de Dados Extras do Facebook:
  SOCIAL_AUTH_FACEBOOK_KEY = "CÓDIGO ID do Aplicativo"
  SOCIAL_AUTH_FACEBOOK_SECRET = "Chave Secreta do Aplicativo"
  SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']
  SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
      'fields': 'id, name, email, picture.type(large), link'
  }
  SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
      ('name', 'name'), ('email', 'email'),
      ('picture', 'picture'), ('link', 'profile_url'),
  ]
  ```
- **🎤 O que falar para o professor:**
  > *"Para o Facebook, além do App ID e App Secret configurados para o domínio `localhost:8000`, adicionamos os context processors do `social_django` e configuramos o `SCOPE` e o `EXTRA_DATA` para solicitar nome, e-mail, foto de perfil e link do usuário."*

---

### 🌐 Slide 7 — Etapa 12.3: Configuração do Google OAuth 2.0
- **Arquivo modificado:** `lojaAdmin/settings/settings.py` e `loja/templates/auth/auth.html`
- **Tópicos do Slide:**
  - Criação do projeto e **Tela de Consentimento OAuth (Externo)** no Google Cloud Console.
  - Criação do **ID do Cliente OAuth (Aplicativo da Web)**.
  - **URI de redirecionamento autorizado obrigatório:**
    `http://localhost:8000/social-auth/complete/google-oauth2/`
- **Código para colocar no Slide:**
  ```python
  # lojaAdmin/settings/settings.py
  SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'Seu ID de cliente'
  SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Sua chave secreta de cliente'
  ```

---

### 🖥️ Slide 8 — Demonstração Visual no Sistema LojaPSI
- **Telas para mostrar lado a lado no Slide:**
  1. **Tela de Login (`/login/`):** Card moderno com login tradicional + botões Facebook e Google.
  2. **Tela de Registro (`/register/`):** Mesma estrutura reutilizando `auth.html`.
  3. **Tela de Edição de Perfil (`/usuario/edit`):** Exibe os dados do `User` e `Usuario`, além do bloco `backends.associated` quando há conta social vinculada.
  4. **Painel Django Admin (`/admin/social_django/usersocialauth/`):** Gerenciamento de vínculos sociais (`User social auths`).

---

### ✅ Slide 9 — Conclusão
- **Resumo do que foi alcançado:**
  - Integração completa do `social-auth-app-django` ao `LojaPSI`.
  - Criação automática do perfil `Usuario` via `post_save` signal quando um usuário social é criado no Django.
  - Interface responsiva, moderna e fiel à lógica do Capítulo 12.
