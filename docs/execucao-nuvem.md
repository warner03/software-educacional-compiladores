# Execução em nuvem com proxy TLS

Em computadores com Docker em rede comum, use os comandos padrão do README. O override abaixo é opcional e atende ambientes que fornecem uma CA confiável para o proxy HTTPS.

Na máquina desta sessão, o bundle do sistema inclui a CA do proxy. Do diretório do repositório:

```bash
export CLOUD_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
export COMPOSE_FILE=docker-compose.yml:compose.cloud.yaml

docker compose build backend frontend testes-frontend
docker compose up -d --wait
python3 scripts/registrar_testes.py --integracao --navegador --chromium /usr/bin/chromium
```

O caminho do Chromium é específico da máquina; em outro ambiente, instale Playwright como no README ou informe seu navegador. O bundle deve ser o fornecido e confiável no ambiente em uso, não um certificado arbitrário. No Windows, utilize a forma de combinar arquivos suportada pelo Compose local e um caminho válido para seu bundle.

Os Dockerfiles montam a CA apenas durante instalação (`PIP_CERT`/`NODE_EXTRA_CA_CERTS`). Sem o secret opcional, utilizam a confiança padrão das imagens. A verificação TLS permanece ativa. Não há chave ou valor de credencial neste repositório.

O healthcheck wget usa conexão direta apenas para o loopback dentro do contêiner; isso evita encaminhar a verificação local ao proxy. Instalações externas continuam respeitando o proxy do ambiente. A permissão dos arquivos copiados para o nginx é definida como 644 dentro da imagem.

Para simular reconstrução das dependências a partir de imagens base, sem reutilizar camadas de build:

```bash
docker compose build --no-cache backend frontend testes-frontend
```

Isso não equivale a validar uma máquina de outro sistema operacional. Os testes desta sessão usam Linux com Docker; os resultados estão no registro de testes. Use o checkout já fornecido pela tarefa; não é necessário criar git worktree.
