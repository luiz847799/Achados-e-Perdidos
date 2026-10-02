# Achados & Perdidos

Mini aplicação web acadêmica desenvolvida com **Python, Flask, SQLite, HTML, CSS e JavaScript**.

## Funcionalidades

- Cadastro de itens perdidos ou encontrados.
- Campos de nome, descrição, local e contato.
- Listagem dos itens cadastrados.
- Marcação de item como devolvido/resolvido e opção de reabertura.
- Filtros: Todos, Perdidos e Encontrados.
- Busca por palavra-chave no nome, descrição e local.
- Mensagens de feedback após as ações.
- Upload opcional de imagem (PNG, JPG, JPEG, GIF e WEBP; até 5 MB).

## Requisitos

- Python 3.10 ou superior
- pip

## Como executar localmente

1. Extraia o arquivo ZIP e entre na pasta do projeto.
2. (Opcional, recomendado) Crie e ative um ambiente virtual:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **Linux/macOS:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a aplicação:

   ```bash
   python app.py
   ```

5. Abra `http://127.0.0.1:5000` no navegador.

O banco `achados_perdidos.db` é criado automaticamente na primeira execução. As imagens enviadas ficam em `static/uploads/`.

## Estrutura do projeto

```text
achados_e_perdidos/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── uploads/
        └── .gitkeep
```

## Publicar no GitHub

Crie um repositório vazio no GitHub e, dentro da pasta do projeto, execute:

```bash
git init
git add .
git commit -m "Adiciona mini app Achados e Perdidos"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/achados-e-perdidos.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu nome de usuário do GitHub. Depois, envie o link do repositório ao professor pelo e-mail indicado na atividade.

## Observações

- Este projeto é uma versão didática. Antes de publicar para uso real, altere a `SECRET_KEY`, adicione proteção contra abuso e configure o servidor para produção.
- Os dados de contato são exibidos no mural; utilize apenas informações apropriadas para o contexto da atividade.
- O banco de dados local não é enviado ao GitHub.
