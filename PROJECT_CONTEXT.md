# SEXTA-FEIRA --- Contexto do Projeto

> Documento compartilhado de contexto para ChatGPT, Gemini e Claude.
> **Objetivo:** manter uma única fonte de verdade sobre o projeto,
> reduzir decisões contraditórias e facilitar a continuidade do
> desenvolvimento.
>
> **Status deste documento:** primeira versão, elaborada a partir do
> contexto fornecido pelo proprietário do projeto em 18/11/2026.
> Informações sobre o estado real do repositório e do ambiente local
> devem ser verificadas antes de qualquer alteração.

------------------------------------------------------------------------

## 1. Identidade e objetivo

**Nome:** SEXTA-FEIRA\
**Repositório oficial:** https://github.com/matheussaf/SEXTA-FEIRA\
**Idioma da assistente:** português brasileiro\
**Plataforma inicial desejada:** Windows\
**Responsável pelo projeto e decisões finais:** Matheus

A SEXTA-FEIRA é uma assistente virtual pessoal. A intenção é evoluir o
backend já iniciado para um aplicativo desktop próprio, que possa
permanecer em segundo plano no Windows, ser acessado pela bandeja do
sistema (system tray) e oferecer uma interface de conversação.

A visão de longo prazo inclui conversação natural, ferramentas externas,
memória, voz e automação do computador. Esses recursos são objetivos de
evolução, não devem ser tratados como implementados sem evidência no
código.

### Princípios do produto

-   Ter identidade própria e conversar em português brasileiro.
-   Separar o núcleo da assistente da interface visual.
-   Evoluir incrementalmente, preservando o que já funciona.
-   Preferir componentes simples, testáveis e substituíveis.
-   Não adicionar funcionalidades sem definir escopo, permissões e
    critérios de aceitação.
-   Manter credenciais fora do código e do controle de versão.
-   Solicitar confirmação antes de ações sensíveis no computador.

------------------------------------------------------------------------

## 2. Estado conhecido do projeto

As informações abaixo vêm do relatório fornecido pelo proprietário. Elas
descrevem o estado relatado, não substituem uma inspeção atual do
repositório.

### 2.1 Relatado como implementado ou funcional

-   Backend em Python utilizando FastAPI.
-   Integração com a API da Groq por meio da biblioteca `groq`.
-   Carregamento de variáveis de ambiente com `python-dotenv`.
-   Endpoint `GET /` para informar o status do backend.
-   Endpoint `POST /chat` para receber uma mensagem e retornar uma
    resposta.
-   Integração inicial com a API Open-Meteo para consultar o clima de
    Santos, SP.
-   Uso de Git e GitHub, com a branch principal informada como `main`.
-   Arquivo `.gitignore` configurado para ignorar `.env`, ambiente
    virtual e arquivos de cache, segundo o histórico relatado.
-   README atualizado com instruções de execução e tecnologias
    utilizadas, segundo o histórico relatado.

O proprietário informou que o backend respondeu com `200 OK`. Isso não
significa, por si só, que todos os fluxos, erros e integrações tenham
sido testados.

### 2.2 Estrutura local informada

A estrutura relatada no momento da elaboração deste documento é:

``` text
SEXTA-FEIRA/
├── assets/
│   └── logo.png
├── backend/
│   ├── main.py
│   └── requirements.txt
├── .env
├── .gitignore
└── README.md
```

O caminho local mencionado no histórico foi
`C:\Users\dougl\OneDrive\Desktop\SEXTA-FEIRA`. **Verificar o caminho
real antes de executar comandos ou editar arquivos.**

### 2.3 Tecnologias mencionadas

  -----------------------------------------------------------------------
  Área                    Tecnologia / serviço    Situação
  ----------------------- ----------------------- -----------------------
  Linguagem               Python                  Informado como
                                                  utilizado

  API local               FastAPI                 Relatado como
                                                  implementado

  Servidor ASGI           Uvicorn                 Informado na stack;
                                                  confirmar configuração

  Provedor de IA          Groq API                Relatado como integrado

  Biblioteca de IA        `groq`                  Utilizada no código
                                                  compartilhado

  Variáveis de ambiente   `python-dotenv`         Utilizada no código
                                                  compartilhado

  Requisições HTTP        `requests`              Utilizada no código
                                                  compartilhado

  Validação de dados      Pydantic                Utilizada no código
                                                  compartilhado

  Clima                   Open-Meteo              Relatado como integrado

  Versionamento           Git / GitHub            Relatado como utilizado

  Gerenciamento de        `uv` e/ou `pip`         Ambos mencionados;
  pacotes                                         confirmar fluxo adotado
  -----------------------------------------------------------------------

A versão Python foi informada como **3.15**, mas deve ser conferida no
ambiente real (`python --version`) e comparada com a compatibilidade das
dependências antes de fixar essa versão na documentação.

------------------------------------------------------------------------

## 3. Backend conhecido

O proprietário compartilhou uma versão de `backend/main.py` com o
seguinte comportamento:

1.  Carrega variáveis do arquivo `.env`.
2.  Obtém uma chave de API.
3.  Cria um cliente `Groq`.
4.  Consulta a lista de modelos disponíveis e seleciona o primeiro cujo
    identificador não contenha `whisper` ou `guard`.
5.  Cria uma aplicação FastAPI.
6.  Define um modelo Pydantic `MensagemRequest` com o campo `texto`.
7.  Consulta a Open-Meteo para as coordenadas de Santos quando a
    mensagem contém palavras como `clima`, `tempo` ou `temperatura`.
8.  Para outras mensagens, envia uma chamada de chat à Groq com uma
    instrução de sistema que define a identidade da SEXTA-FEIRA.
9.  Retorna a resposta em JSON.

### 3.1 Endpoints informados

-   `GET /`: retorna status, modelo ativo e mensagem de funcionamento.
-   `POST /chat`: recebe `{ "texto": "..." }` e devolve a resposta da
    assistente.

### 3.2 Observações técnicas que precisam ser verificadas/corrigidas

O trecho de código compartilhado é uma fotografia do estado relatado
naquele momento. Antes de implementar novas funcionalidades, comparar
com o arquivo atual do repositório.

-   **Caminho do `.env`:** `load_dotenv(dotenv_path="../.env")` depende
    do diretório de execução. Preferir um caminho resolvido a partir da
    localização do arquivo ou uma configuração explícita e documentada.
-   **Chave de API:** o código compartilhado usa `GROQ_API_KEY` ou, como
    fallback, `GEMINI_API_KEY`, mas instancia `Groq` em ambos os casos.
    Uma chave Gemini não autentica na Groq. Remover esse fallback ou
    implementar provedores separados com clientes próprios.
-   **Descoberta de modelos:** excluir apenas identificadores contendo
    `whisper` ou `guard` não garante compatibilidade com chat. Usar uma
    lista de modelos suportados/configuráveis, validar a capacidade
    necessária e manter um fallback conhecido e atualizado.
-   **Tratamento de exceções:** evitar retornar detalhes internos e
    mensagens brutas de provedores ao cliente em produção. Registrar
    detalhes de forma segura no log e retornar mensagens apropriadas.
-   **HTTP da Open-Meteo:** definir timeout, verificar status HTTP
    (`raise_for_status()`), validar a presença dos campos esperados e
    tratar falhas de rede/JSON.
-   **Roteamento por palavras-chave:** a detecção de clima por
    `if "clima" ...` é uma regra inicial simples. À medida que
    ferramentas aumentarem, migrar para um roteador de
    intenções/ferramentas mais explícito.
-   **Histórico:** o código compartilhado envia somente a mensagem atual
    e a instrução de sistema. Não há memória conversacional persistente
    demonstrada nesse trecho.
-   **Dependências:** conferir `requirements.txt` atual. O código
    compartilhado importa `groq`, `python-dotenv`, `requests`, `fastapi`
    e `pydantic`; a execução também requer um servidor ASGI como
    Uvicorn. Garantir que todas as dependências necessárias estejam
    declaradas e, idealmente, com versões compatíveis.
-   **Validação de entrada:** definir limites para o tamanho de `texto`
    e respostas para mensagens vazias.
-   **Configuração:** mover coordenadas, modelo preferencial, host/porta
    e outras opções para configurações centralizadas, sem colocar
    segredos no repositório.

Nenhuma dessas observações deve ser considerada corrigida até que o
código e os testes confirmem a correção.

------------------------------------------------------------------------

## 4. Arquitetura-alvo para o aplicativo Windows

O próximo objetivo de produto é criar uma aplicação desktop que possa
permanecer na bandeja do sistema e abrir uma janela de chat.

### 4.1 Direção arquitetural

Manter responsabilidades separadas:

``` text
SEXTA-FEIRA/
├── assets/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── desktop/
│   ├── tray.py
│   ├── window.py
│   └── ...
├── docs/
├── tests/
├── .env
├── .gitignore
├── PROJECT_CONTEXT.md
└── README.md
```

Esta é uma **estrutura sugerida**, não a estrutura atual confirmada. Não
criar todos esses arquivos de uma vez sem um plano aprovado.

### 4.2 Componentes planejados

  -----------------------------------------------------------------------
  Componente              Opção considerada       Responsabilidade
  ----------------------- ----------------------- -----------------------
  System tray             `pystray`               Ícone e menu na bandeja
                                                  do Windows

  Imagens/ícones          `Pillow`                Carregar e preparar o
                                                  ícone

  Backend local           FastAPI + Uvicorn       Expor a API local da
                                                  assistente

  Interface               HTML, CSS e JavaScript  Janela de chat e
                                                  configurações

  Janela desktop          `pywebview` ou          Exibir a interface como
                          `PySide6`               janela nativa

  Empacotamento           PyInstaller             Gerar executável
                                                  distribuível
  -----------------------------------------------------------------------

As opções acima ainda precisam ser avaliadas e aprovadas. Não assumir
que todas serão usadas. Em particular, escolher entre `pywebview` e
`PySide6` após um pequeno protótipo, considerando manutenção, tamanho,
experiência de desenvolvimento e integração com o Windows.

### 4.3 Comportamento esperado do primeiro desktop

-   Iniciar sem exigir que o usuário abra o VS Code.
-   Executar em segundo plano.
-   Exibir um ícone na bandeja do Windows.
-   Oferecer opções como **Abrir**, **Reiniciar** e **Sair**.
-   Abrir uma janela própria de conversação.
-   Comunicar-se com o backend local.
-   Permitir encerramento limpo dos processos.
-   Preparar, posteriormente, uma opção de inicialização com o Windows.

A inicialização automática deve ser opcional e configurável pelo
usuário. O aplicativo deve deixar claro quando está ativo e como
encerrá-lo.

------------------------------------------------------------------------

## 5. Roadmap proposto

O roadmap abaixo é uma proposta de sequência. O status deve ser
atualizado conforme cada etapa for concluída e testada.

  -----------------------------------------------------------------------
  Etapa                   Entrega                 Status inicial
  ----------------------- ----------------------- -----------------------
  0                       Inspecionar e registrar Pendente
                          o estado real do        
                          repositório             

  1                       Corrigir configuração,  Pendente
                          dependências e robustez 
                          do backend              

  2                       Criar o processo        Planejado
                          desktop e o ícone de    
                          system tray             

  3                       Criar janela de chat e  Planejado
                          conectar ao backend     
                          local                   

  4                       Implementar histórico e Planejado
                          memória de conversas    

  5                       Criar sistema           Planejado
                          organizado de           
                          ferramentas (tools)     

  6                       Adicionar voz:          Futuro
                          reconhecimento e        
                          síntese                 

  7                       Adicionar automações do Futuro
                          Windows com permissões  

  8                       Empacotar, instalar e   Futuro
                          configurar              
                          inicialização opcional  
  -----------------------------------------------------------------------

### Critérios mínimos para considerar o Desktop v1.0 concluído

-   O aplicativo inicia sem abrir o VS Code.
-   O ícone aparece na bandeja do Windows.
-   O menu abre e encerra a aplicação corretamente.
-   A janela de chat abre e fecha sem deixar processos órfãos.
-   A interface consegue enviar uma mensagem ao backend e mostrar a
    resposta.
-   Erros de conexão são apresentados de forma compreensível.
-   O encerramento limpa os processos e libera a porta utilizada.
-   As credenciais permanecem fora do executável/repositório e são
    tratadas com segurança.
-   O funcionamento foi testado no Windows do proprietário.

------------------------------------------------------------------------

## 6. Divisão de responsabilidades entre as IAs

As três IAs são colaboradoras com papéis distintos. **Matheus é o
responsável pelo produto e toma as decisões finais.**

### ChatGPT --- Arquiteto e revisor técnico

Responsabilidades:

-   Manter a visão geral do projeto.
-   Planejar funcionalidades e dividir o trabalho em etapas.
-   Propor e avaliar arquitetura.
-   Revisar implementações e decisões técnicas.
-   Identificar riscos, inconsistências e regressões.
-   Definir critérios de aceitação e testes.
-   Consolidar decisões aprovadas neste documento.

Não deve presumir que algo foi implementado sem verificar evidências.
Não deve recomendar reescritas amplas sem justificativa.

### Gemini --- Pesquisador técnico

Responsabilidades:

-   Pesquisar documentação oficial e bibliotecas.
-   Investigar erros específicos.
-   Comparar tecnologias e alternativas.
-   Verificar compatibilidade de versões e APIs.
-   Apresentar vantagens, desvantagens, limitações e fontes.

Deve separar fatos documentados de hipóteses. Não deve alterar a
arquitetura por conta própria nem apresentar uma API como compatível sem
verificar.

### Claude --- Engenheiro de implementação

Responsabilidades:

-   Inspecionar os arquivos antes de alterá-los.
-   Implementar especificações aprovadas.
-   Criar e modificar módulos.
-   Desenvolver interface e funcionalidades.
-   Escrever e executar testes quando possível.
-   Informar arquivos alterados, dependências e resultados reais.

Não deve reescrever arquivos inteiros sem necessidade, remover
funcionalidades ou mudar decisões arquiteturais sem aprovação.

### Matheus --- Proprietário e responsável pelas decisões

Responsabilidades:

-   Definir prioridades e experiência desejada.
-   Aprovar decisões que alterem arquitetura ou escopo.
-   Testar o aplicativo no ambiente real.
-   Revisar as alterações antes de integrá-las.
-   Aprovar commits e releases.

------------------------------------------------------------------------

## 7. Fluxo de trabalho padrão

Para cada funcionalidade:

1.  **Definição:** Matheus descreve o resultado desejado.
2.  **Planejamento:** ChatGPT propõe escopo, arquitetura, arquivos
    envolvidos e critérios de aceitação.
3.  **Pesquisa:** Gemini investiga dúvidas técnicas e fornece
    fontes/documentação.
4.  **Validação:** ChatGPT consolida as informações e apresenta uma
    proposta técnica.
5.  **Aprovação:** Matheus aprova ou ajusta o plano.
6.  **Implementação:** Claude implementa o escopo aprovado.
7.  **Revisão:** ChatGPT analisa o diff, a aderência à arquitetura e os
    riscos.
8.  **Teste:** Matheus executa os testes no Windows; a IA responsável
    registra apenas os testes que realmente executou.
9.  **Versionamento:** após aprovação, Matheus realiza o commit e
    atualiza este documento.

### Regras de colaboração

-   Não pedir às três IAs para editar simultaneamente o mesmo arquivo.
-   Não aceitar alterações sem saber quais arquivos foram modificados.
-   Não copiar código de uma IA para o projeto sem revisão e teste.
-   Ao solicitar ajuda a outra IA, fornecer este documento e os arquivos
    relevantes.
-   Se uma IA sugerir uma mudança arquitetural, registrar a proposta e
    obter aprovação antes de implementá-la.
-   Se o código real contradisser este documento, inspecionar o código e
    atualizar o documento após confirmar o estado correto.

------------------------------------------------------------------------

## 8. Padrões de implementação e segurança

-   Manter segredos em `.env` ou em mecanismo seguro apropriado; nunca
    versionar credenciais.
-   Manter `.env.example` sem valores secretos, documentando apenas os
    nomes das variáveis necessárias.
-   Não registrar chaves, tokens ou conteúdo sensível em logs.
-   Validar todas as entradas recebidas pela API.
-   Usar timeouts e tratamento de falhas em chamadas externas.
-   Restringir o backend local a uma interface local por padrão; não
    expor a API na rede sem necessidade e proteção adequada.
-   Considerar autenticação ou token local para operações sensíveis,
    mesmo em aplicações locais.
-   Solicitar confirmação explícita para ações destrutivas, envio de
    mensagens, alterações de arquivos ou outras operações relevantes.
-   Aplicar princípio do menor privilégio às automações do Windows.
-   Separar lógica de negócio, integração com provedores, ferramentas,
    interface e configuração.
-   Evitar dependências desnecessárias e registrar por que cada nova
    biblioteca foi adicionada.
-   Não afirmar que testes passaram sem executá-los.

------------------------------------------------------------------------

## 9. Como atualizar este documento

Este arquivo é uma fonte de contexto compartilhada, não um registro
automático do repositório.

Atualizar quando houver:

-   Nova decisão arquitetural aprovada.
-   Mudança de tecnologia ou dependência.
-   Funcionalidade concluída e testada.
-   Alteração relevante na estrutura de pastas.
-   Mudança no fluxo de desenvolvimento.
-   Problema conhecido ou limitação descoberta.

Ao marcar algo como concluído, registrar evidência breve: teste
executado, comportamento observado ou arquivo/endpoint confirmado.

### Modelo de registro de decisão

``` text
Data:
Decisão:
Contexto / motivo:
Alternativas consideradas:
Consequências:
Aprovado por:
Status:
```

### Histórico deste documento

-   **2026-11-18:** primeira versão criada com base no relatório e nas
    informações fornecidas por Matheus. A estrutura real do repositório,
    o código atual, a versão do Python e o estado de segurança ainda
    precisam ser conferidos.

------------------------------------------------------------------------

## 10. Instrução inicial para qualquer IA que receber este arquivo

Antes de sugerir ou executar alterações:

1.  Leia este documento.
2.  Inspecione o estado atual do repositório e os arquivos relevantes.
3.  Identifique divergências entre o documento e o código.
4.  Não trate itens planejados como implementados.
5.  Respeite a divisão de responsabilidades e o fluxo de aprovação.
6.  Apresente um plano pequeno e verificável antes de mudanças
    significativas.
7.  Preserve funcionalidades existentes e explique qualquer alteração de
    comportamento.

**Objetivo comum:** construir a SEXTA-FEIRA de forma incremental,
segura, testável e coerente, mantendo Matheus no controle das decisões
do projeto.
