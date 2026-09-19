#!/usr/bin/env python3
"""Gera os dois PDFs finais do desafio a partir dos artefatos do projeto."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TMP = ROOT.parent / "tmp" / "pdfs" / "generated_diagrams"
REPORT_PATH = DOCS / "entregavel-final-arquitetura-software.pdf"
DIAGRAMS_PATH = DOCS / "diagramas-arquitetura.pdf"

NAVY = colors.HexColor("#15324B")
BLUE = colors.HexColor("#176B87")
TEAL = colors.HexColor("#2A9D8F")
ORANGE = colors.HexColor("#F4A261")
GOLD = colors.HexColor("#E9C46A")
INK = colors.HexColor("#243746")
MUTED = colors.HexColor("#60758A")
PALE_BLUE = colors.HexColor("#EAF1F6")
PALE_TEAL = colors.HexColor("#EAF7F2")
PALE_GOLD = colors.HexColor("#FFF8E8")
PALE_RED = colors.HexColor("#FCE7EC")
LIGHT = colors.HexColor("#F7FAFC")
LINE = colors.HexColor("#D5E0E8")
WHITE = colors.white


def register_fonts():
    pdfmetrics.registerFont(
        TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    )


register_fonts()

BASE = getSampleStyleSheet()
STYLES = {
    "cover_kicker": ParagraphStyle(
        "cover_kicker",
        fontName="DejaVu-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#9EE6DD"),
        spaceAfter=14,
    ),
    "cover_title": ParagraphStyle(
        "cover_title",
        fontName="DejaVu-Bold",
        fontSize=31,
        leading=38,
        textColor=WHITE,
        spaceAfter=16,
    ),
    "cover_subtitle": ParagraphStyle(
        "cover_subtitle",
        fontName="DejaVu",
        fontSize=15,
        leading=22,
        textColor=colors.HexColor("#D9E8F2"),
        spaceAfter=25,
    ),
    "cover_meta": ParagraphStyle(
        "cover_meta",
        fontName="DejaVu",
        fontSize=10,
        leading=16,
        textColor=WHITE,
    ),
    "h1": ParagraphStyle(
        "h1",
        fontName="DejaVu-Bold",
        fontSize=20,
        leading=25,
        textColor=NAVY,
        spaceAfter=10,
    ),
    "h2": ParagraphStyle(
        "h2",
        fontName="DejaVu-Bold",
        fontSize=12.5,
        leading=16,
        textColor=BLUE,
        spaceBefore=8,
        spaceAfter=6,
    ),
    "body": ParagraphStyle(
        "body",
        fontName="DejaVu",
        fontSize=9.2,
        leading=14,
        textColor=INK,
        spaceAfter=7,
    ),
    "body_small": ParagraphStyle(
        "body_small",
        fontName="DejaVu",
        fontSize=7.6,
        leading=10.6,
        textColor=INK,
    ),
    "body_small_bold": ParagraphStyle(
        "body_small_bold",
        fontName="DejaVu-Bold",
        fontSize=7.6,
        leading=10.6,
        textColor=INK,
    ),
    "caption": ParagraphStyle(
        "caption",
        fontName="DejaVu",
        fontSize=7.7,
        leading=11,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceBefore=5,
        spaceAfter=8,
    ),
    "callout_title": ParagraphStyle(
        "callout_title",
        fontName="DejaVu-Bold",
        fontSize=9.5,
        leading=13,
        textColor=NAVY,
        spaceAfter=3,
    ),
    "callout_body": ParagraphStyle(
        "callout_body",
        fontName="DejaVu",
        fontSize=8.5,
        leading=13,
        textColor=INK,
    ),
    "code": ParagraphStyle(
        "code",
        fontName="Courier",
        fontSize=7.1,
        leading=10,
        textColor=colors.HexColor("#EAF2F7"),
    ),
    "link": ParagraphStyle(
        "link",
        fontName="DejaVu-Bold",
        fontSize=9,
        leading=13,
        textColor=BLUE,
        alignment=TA_LEFT,
    ),
}


def p(text, style="body"):
    return Paragraph(text, STYLES[style])


def section_title(number, title, subtitle=None):
    items = [p(f"{number}. {title}", "h1")]
    if subtitle:
        items.append(
            Paragraph(
                subtitle,
                ParagraphStyle(
                    "section_subtitle",
                    parent=STYLES["body"],
                    fontSize=10,
                    leading=14,
                    textColor=MUTED,
                    spaceAfter=12,
                ),
            )
        )
    return items


def callout(title, text, fill=PALE_TEAL, border=TEAL):
    content = [p(title, "callout_title"), p(text, "callout_body")]
    table = Table([[content]], colWidths=[172 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.8, border),
                ("LINEBEFORE", (0, 0), (0, -1), 4, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def table(data, widths, header=True, font_size=7.4, row_backgrounds=True):
    wrapped = []
    for row_index, row in enumerate(data):
        style = "body_small_bold" if header and row_index == 0 else "body_small"
        wrapped.append([p(str(cell), style) for cell in row])

    result = Table(wrapped, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ]
    if row_backgrounds:
        for row_index in range(1 if header else 0, len(data)):
            if row_index % 2 == 0:
                commands.append(("BACKGROUND", (0, row_index), (-1, row_index), LIGHT))
    result.setStyle(TableStyle(commands))
    return result


def bullets(items):
    rows = []
    for item in items:
        rows.append(
            [
                Paragraph("&#9632;", ParagraphStyle("bullet", parent=STYLES["body"], textColor=TEAL, fontSize=6)),
                p(item, "body"),
            ]
        )
    result = Table(rows, colWidths=[5 * mm, 166 * mm], hAlign="LEFT")
    result.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return result


def code_block(text):
    content = Preformatted(text, STYLES["code"])
    result = Table([[content]], colWidths=[172 * mm])
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#203545")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#152531")),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return result


def first_page(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, height, stroke=0, fill=1)
    canvas.setFillColor(BLUE)
    canvas.circle(width + 15 * mm, height - 28 * mm, 72 * mm, stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.circle(width - 10 * mm, 14 * mm, 52 * mm, stroke=0, fill=1)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, 0, 8 * mm, height, stroke=0, fill=1)
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.18))
    canvas.setLineWidth(1)
    canvas.line(25 * mm, 48 * mm, width - 24 * mm, 48 * mm)
    canvas.setFont("DejaVu", 8)
    canvas.setFillColor(colors.HexColor("#D9E8F2"))
    canvas.drawString(25 * mm, 30 * mm, "Desafio Final - Bootcamp Arquiteto(a) de Software")
    canvas.restoreState()


def later_pages(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 10 * mm, width, 10 * mm, stroke=0, fill=1)
    canvas.setFont("DejaVu-Bold", 7.2)
    canvas.setFillColor(WHITE)
    canvas.drawString(20 * mm, height - 6.5 * mm, "PARTNER PRODUCTS API")
    canvas.setStrokeColor(LINE)
    canvas.line(20 * mm, 15 * mm, width - 20 * mm, 15 * mm)
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9.5 * mm, "Ronoel Lima | Arquitetura MVC em JavaScript")
    canvas.drawRightString(width - 20 * mm, 9.5 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build_report():
    DOCS.mkdir(parents=True, exist_ok=True)
    c4_png = TMP / "c4-conteineres.png"
    mvc_png = TMP / "mvc-componentes.png"
    if not c4_png.exists() or not mvc_png.exists():
        raise FileNotFoundError("As imagens dos diagramas precisam ser exportadas antes do relatório.")

    doc = SimpleDocTemplate(
        str(REPORT_PATH),
        pagesize=A4,
        leftMargin=19 * mm,
        rightMargin=19 * mm,
        topMargin=19 * mm,
        bottomMargin=20 * mm,
        title="Entregável Final - Arquitetura de Software - Partner Products API",
        author="Ronoel Lima",
        subject="API REST MVC em JavaScript com Node.js, Express e SQLite",
    )

    story = []
    story += [
        Spacer(1, 40 * mm),
        p("BOOTCAMP ARQUITETO(A) DE SOFTWARE", "cover_kicker"),
        p("Desafio Final:<br/>Partner Products API", "cover_title"),
        p("Arquitetura MVC, API REST e persistência<br/>implementadas em JavaScript", "cover_subtitle"),
        Spacer(1, 15 * mm),
        Table(
            [
                [p("AUTOR", "cover_meta"), p("Ronoel Lima", "cover_meta")],
                [p("STACK", "cover_meta"), p("Node.js 24 | Express 5 | SQLite | Zod", "cover_meta")],
                [p("ENTREGA", "cover_meta"), p("19 de setembro de 2026", "cover_meta")],
                [p("STATUS", "cover_meta"), p("Implementação funcional - 6 testes aprovados", "cover_meta")],
            ],
            colWidths=[32 * mm, 115 * mm],
            hAlign="LEFT",
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.Color(1, 1, 1, alpha=0.25)),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            ),
        ),
        Spacer(1, 20 * mm),
        Paragraph(
            '<link href="https://github.com/ronoellima10-ship-it/desafio-final-arquiteto-software-api" color="#9EE6DD">github.com/ronoellima10-ship-it/desafio-final-arquiteto-software-api</link>',
            STYLES["cover_meta"],
        ),
        PageBreak(),
    ]

    story += section_title(
        "1",
        "Visão geral e conformidade",
        "Rastreabilidade direta entre o enunciado, a implementação e os arquivos entregues.",
    )
    story += [
        callout(
            "Resultado",
            "Foi construída uma API REST de Produtos seguindo MVC, com todos os endpoints pedidos, persistência SQLite, documentação OpenAPI, testes automatizados, Docker e integração contínua. Os três entregáveis obrigatórios estão consolidados neste PDF e o diagrama permanece editável no draw.io.",
        ),
        Spacer(1, 6 * mm),
        table(
            [
                ["Requisito do enunciado", "Implementação", "Evidência", "Status"],
                ["CRUD completo", "POST, GET, PUT/PATCH e DELETE", "src/routes e testes E2E", "Atendido"],
                ["Contagem", "GET /api/v1/products/count", "Controller + Service + Repository", "Atendido"],
                ["Find All", "GET /api/v1/products", "Listagem ordenada", "Atendido"],
                ["Find By ID", "GET /api/v1/products/:id", "404 quando inexistente", "Atendido"],
                ["Find By Name", "GET /api/v1/products/name/:name", "Busca parcial case-insensitive", "Atendido"],
                ["Padrão MVC", "Model, Controller e representação JSON", "Diagrama e estrutura de código", "Atendido"],
                ["Desenho arquitetural", "C4 + componentes MVC", "draw.io e PDF de diagramas", "Atendido"],
                ["Estrutura e explicação", "Árvore e matriz de responsabilidades", "Seções 5 e 6", "Atendido"],
                ["Código funcional (opcional)", "Node.js + Express", "Repositório GitHub", "Incluído"],
                ["Persistência (opcional)", "SQLite com constraints", "Banco criado automaticamente", "Incluído"],
            ],
            [55 * mm, 52 * mm, 48 * mm, 17 * mm],
        ),
        Spacer(1, 6 * mm),
        p("<b>Entregáveis finais:</b> este relatório, o PDF dos diagramas, o arquivo <font name='Courier'>arquitetura.drawio</font> e o repositório com o código executável.", "body"),
        PageBreak(),
    ]

    story += section_title(
        "2",
        "Contexto, escopo e requisitos",
        "A solução publica dados de produtos de uma empresa de vendas on-line para parceiros externos.",
    )
    story += [
        p("<b>Problema.</b> Parceiros precisam consultar e manter dados de produtos por uma interface pública, previsível e documentada. A aplicação deve separar interface HTTP, regras de negócio e persistência para facilitar evolução e manutenção."),
        p("<b>Escopo.</b> O domínio escolhido é Produto. A primeira versão administra cadastro, descrição, preço, estoque e situação ativa. Autenticação, paginação e banco distribuído ficam fora do escopo acadêmico inicial."),
        p("Requisitos funcionais", "h2"),
        table(
            [
                ["ID", "Requisito", "Critério de aceite"],
                ["RF-01", "Criar produto", "Retorna 201, Location e produto persistido"],
                ["RF-02", "Listar todos", "Retorna 200, coleção e total da resposta"],
                ["RF-03", "Buscar por ID", "Retorna 200 ou 404 padronizado"],
                ["RF-04", "Buscar por nome", "Pesquisa parcial sem diferenciar caixa"],
                ["RF-05", "Atualizar", "Aceita PUT/PATCH e preserva campos não enviados"],
                ["RF-06", "Excluir", "Retorna 204 ou 404"],
                ["RF-07", "Contar", "Retorna o número total de produtos"],
            ],
            [20 * mm, 58 * mm, 94 * mm],
        ),
        Spacer(1, 6 * mm),
        p("Requisitos não funcionais", "h2"),
        table(
            [
                ["ID", "Atributo", "Decisão verificável"],
                ["RNF-01", "Manutenibilidade", "Camadas coesas, dependências unidirecionais e Repository"],
                ["RNF-02", "Confiabilidade", "Validação, constraints SQLite e encerramento controlado"],
                ["RNF-03", "Segurança básica", "Helmet, CORS configurável, JSON limitado e sem detalhes internos em produção"],
                ["RNF-04", "Observabilidade", "Health check e identificador por requisição"],
                ["RNF-05", "Portabilidade", "Execução local ou Docker com variáveis de ambiente"],
                ["RNF-06", "Testabilidade", "SQLite em memória e testes de integração automatizados"],
            ],
            [20 * mm, 40 * mm, 112 * mm],
        ),
        PageBreak(),
    ]

    story += section_title(
        "3",
        "Arquitetura do software - C4",
        "Visão de contêineres do sistema e suas relações em tempo de execução.",
    )
    story += [
        Image(str(c4_png), width=172 * mm, height=96.75 * mm),
        p("Figura 1 - C4 Nível 2: parceiro, API REST, persistência, documentação e operação.", "caption"),
        table(
            [
                ["Elemento", "Tecnologia", "Responsabilidade"],
                ["Parceiro", "Cliente HTTP", "Consome operações REST via HTTPS e JSON"],
                ["API REST", "Node.js + Express", "Expõe o contrato, coordena casos de uso e devolve representações"],
                ["Banco", "SQLite", "Persiste produtos, unicidade do nome e integridade dos valores"],
                ["Documentação", "OpenAPI + Swagger UI", "Torna endpoints e schemas exploráveis"],
                ["Operação", "Docker + CI", "Empacota, verifica saúde e executa testes automaticamente"],
            ],
            [34 * mm, 45 * mm, 93 * mm],
        ),
        Spacer(1, 5 * mm),
        callout(
            "Decisão de desacoplamento",
            "A API não acessa SQLite a partir do Controller. O Repository é a fronteira da persistência. Assim, migrar para PostgreSQL exige uma nova implementação de repositório, preservando casos de uso e contrato HTTP.",
            PALE_GOLD,
            colors.HexColor("#D6A73A"),
        ),
        PageBreak(),
    ]

    story += section_title(
        "4",
        "Arquitetura MVC e fluxo da requisição",
        "Detalhamento dos componentes internos e dependências permitidas.",
    )
    story += [
        Image(str(mvc_png), width=172 * mm, height=96.75 * mm),
        p("Figura 2 - Fluxo HTTP pelos componentes do padrão MVC adaptado à API REST.", "caption"),
        callout(
            "Como o MVC aparece nesta API",
            "<b>Model:</b> entidade, validação e persistência de Produto. <b>Controller:</b> traduz HTTP para chamadas de caso de uso e define a resposta. <b>View:</b> representação JSON entregue ao parceiro. Service e Repository refinam a separação para manter regras e detalhes de infraestrutura fora do Controller.",
        ),
        Spacer(1, 5 * mm),
        p("Direção das dependências", "h2"),
        bullets(
            [
                "Routes conhece Controller; Controller conhece Service; Service conhece Repository.",
                "Repository conhece a conexão SQLite, mas nenhum componente anterior executa SQL.",
                "Middlewares tratam preocupações transversais sem misturá-las às regras do domínio.",
                "Erros de aplicação são convertidos em um contrato HTTP uniforme no limite externo.",
            ]
        ),
        PageBreak(),
    ]

    story += section_title(
        "5",
        "Estrutura de pastas MVC",
        "Organização física do projeto e localização de cada responsabilidade.",
    )
    tree = """desafio-final-arquiteto-software-api/
|-- .github/workflows/ci.yml
|-- data/.gitkeep
|-- docs/
|   |-- arquitetura.drawio
|   |-- diagramas/
|   |-- diagramas-arquitetura.pdf
|   `-- entregavel-final-arquitetura-software.pdf
|-- scripts/
|   |-- generate_report.py
|   `-- seed.js
|-- src/
|   |-- config/          # Banco e contrato OpenAPI
|   |-- controllers/     # Entrada e saída HTTP
|   |-- errors/          # Erros da aplicação
|   |-- middlewares/     # Segurança, contexto e erros
|   |-- models/          # Entidade e validação
|   |-- repositories/    # SQL e persistência
|   |-- routes/          # Endpoints REST
|   |-- services/        # Casos de uso e regras
|   |-- app.js           # Composição das dependências
|   `-- server.js        # Processo HTTP
|-- tests/               # Integração ponta a ponta
|-- Dockerfile
|-- compose.yaml
|-- package.json
`-- README.md"""
    story += [
        code_block(tree),
        Spacer(1, 7 * mm),
        p("Princípios aplicados", "h2"),
        table(
            [
                ["Princípio", "Aplicação no projeto"],
                ["Responsabilidade única", "Cada pasta expressa uma razão principal de mudança"],
                ["Separação de interesses", "HTTP, negócio, validação e dados permanecem isolados"],
                ["Inversão por composição", "app.js cria e injeta Repository, Service e Controller"],
                ["Baixo acoplamento", "O Controller não conhece SQL nem detalhes do SQLite"],
                ["Alta coesão", "Regras do domínio de Produto ficam centralizadas no Service e Model"],
            ],
            [53 * mm, 119 * mm],
        ),
        PageBreak(),
    ]

    story += section_title(
        "6",
        "Componentes e responsabilidades",
        "Explicação dos elementos que compõem o código, conforme solicitado no enunciado.",
    )
    story += [
        table(
            [
                ["Componente", "Arquivo principal", "Responsabilidade", "Não deve fazer"],
                ["Route", "product.routes.js", "Mapear método/URL e encaminhar", "Implementar regra ou SQL"],
                ["Controller", "product.controller.js", "Ler request, chamar Service e formar response", "Conhecer banco"],
                ["Service", "product.service.js", "Executar casos de uso, validar e tratar conflitos", "Manipular HTTP"],
                ["Model", "product.model.js", "Definir contrato e validar Produto", "Responder requisições"],
                ["Repository", "product.repository.js", "Executar SQL e mapear linhas", "Definir status HTTP"],
                ["Database", "database.js", "Conectar, criar tabela, índice e constraints", "Conter regra de fluxo"],
                ["Middleware", "error.middleware.js", "Padronizar erros e preocupações transversais", "Conter caso de uso"],
                ["Composition Root", "app.js", "Montar dependências e pipeline Express", "Misturar regra de domínio"],
                ["Server", "server.js", "Abrir porta e encerrar recursos", "Construir endpoints"],
            ],
            [28 * mm, 38 * mm, 61 * mm, 45 * mm],
        ),
        Spacer(1, 7 * mm),
        callout(
            "Exemplo de colaboração",
            "No POST /products, a Route seleciona create; o Controller recebe o corpo; o Service valida e impede nome duplicado; o Repository executa INSERT; o Controller retorna 201 e o cabeçalho Location. Nenhuma camada assume responsabilidades das demais.",
            PALE_BLUE,
            BLUE,
        ),
        Spacer(1, 7 * mm),
        p("Composição das dependências", "h2"),
        code_block(
            "db -> ProductRepository -> ProductService -> ProductController\n"
            "                               |\n"
            "                               `-> ProductRouter -> Express"
        ),
        PageBreak(),
    ]

    story += section_title(
        "7",
        "Modelo de domínio e persistência",
        "Contrato de Produto, invariantes e decisões de armazenamento.",
    )
    story += [
        table(
            [
                ["Campo", "Tipo", "Regra", "Persistência"],
                ["id", "UUID", "Gerado pela aplicação e imutável", "TEXT PRIMARY KEY"],
                ["name", "String", "2 a 120 caracteres; único sem diferenciar caixa", "TEXT UNIQUE COLLATE NOCASE"],
                ["description", "String", "Opcional; até 500 caracteres", "TEXT NOT NULL DEFAULT ''"],
                ["price", "Number", "Finito; entre 0 e 999.999.999,99", "REAL CHECK price >= 0"],
                ["stock", "Integer", "Entre 0 e 1.000.000", "INTEGER CHECK stock >= 0"],
                ["active", "Boolean", "Padrão true", "INTEGER CHECK active IN (0,1)"],
                ["createdAt", "ISO 8601", "Definido na criação", "TEXT NOT NULL"],
                ["updatedAt", "ISO 8601", "Atualizado a cada alteração", "TEXT NOT NULL"],
            ],
            [28 * mm, 27 * mm, 67 * mm, 50 * mm],
        ),
        Spacer(1, 7 * mm),
        p("Regras de negócio", "h2"),
        bullets(
            [
                "Um nome identifica comercialmente um produto e não pode se repetir, mesmo com variação de maiúsculas.",
                "Preço e estoque nunca podem ser negativos; estoque deve ser inteiro.",
                "Atualização parcial exige pelo menos um campo reconhecido.",
                "Leitura, atualização ou exclusão de ID inexistente retorna NOT_FOUND.",
                "Pesquisa por nome usa correspondência parcial e escapa curingas de SQL LIKE.",
            ]
        ),
        Spacer(1, 7 * mm),
        callout(
            "Persistência como diferencial",
            "O banco é criado automaticamente na primeira execução. Em testes, a mesma implementação usa SQLite em memória. Em produção acadêmica, o arquivo fica em volume Docker. A integridade é aplicada tanto no Model quanto no banco.",
            PALE_GOLD,
            colors.HexColor("#D6A73A"),
        ),
        PageBreak(),
    ]

    story += section_title(
        "8",
        "Contrato da API REST",
        "Endpoints versionados e semântica HTTP previsível para os parceiros.",
    )
    story += [
        table(
            [
                ["Método", "Endpoint", "Sucesso", "Finalidade"],
                ["GET", "/health", "200", "Verificar disponibilidade"],
                ["GET", "/api/v1/products", "200", "Listar todos os produtos"],
                ["GET", "/api/v1/products/count", "200", "Contar registros"],
                ["GET", "/api/v1/products/:id", "200", "Buscar por ID"],
                ["GET", "/api/v1/products/name/:name", "200", "Pesquisar por nome"],
                ["POST", "/api/v1/products", "201", "Criar produto"],
                ["PUT", "/api/v1/products/:id", "200", "Atualizar produto"],
                ["PATCH", "/api/v1/products/:id", "200", "Atualizar parcialmente"],
                ["DELETE", "/api/v1/products/:id", "204", "Excluir produto"],
                ["GET", "/docs", "200", "Abrir Swagger UI"],
                ["GET", "/openapi.json", "200", "Obter contrato OpenAPI"],
            ],
            [23 * mm, 79 * mm, 22 * mm, 48 * mm],
        ),
        Spacer(1, 7 * mm),
        p("Convenções de resposta", "h2"),
        code_block(
            '{\n  "data": { "id": "...", "name": "Notebook Pro 14", "price": 5499.90 }\n}\n\n'
            '{\n  "error": {\n    "code": "VALIDATION_ERROR",\n    "message": "Os dados enviados são inválidos.",\n    "details": [{ "field": "price", "message": "O preço não pode ser negativo." }],\n    "requestId": "..."\n  }\n}'
        ),
        Spacer(1, 6 * mm),
        p("<b>Códigos de erro:</b> 404 para recurso/rota ausente; 409 para conflito de nome; 422 para entrada inválida; 500 para falha inesperada. Toda resposta recebe <font name='Courier'>x-request-id</font> para correlação."),
        PageBreak(),
    ]

    story += section_title(
        "9",
        "Fluxos principais",
        "Sequências essenciais do comportamento da aplicação.",
    )
    story += [
        p("Criar produto", "h2"),
        table(
            [
                ["Passo", "Componente", "Ação"],
                ["1", "Cliente", "Envia POST com JSON"],
                ["2", "Middlewares", "Atribuem request ID, segurança, CORS e fazem parse"],
                ["3", "Route/Controller", "Selecionam a operação e adaptam a entrada"],
                ["4", "Service/Model", "Validam campos e consultam duplicidade"],
                ["5", "Repository/SQLite", "Persistem dentro das constraints"],
                ["6", "Controller", "Retorna 201, Location e representação JSON"],
            ],
            [18 * mm, 46 * mm, 108 * mm],
        ),
        Spacer(1, 6 * mm),
        p("Pesquisar por nome", "h2"),
        table(
            [
                ["Passo", "Ação e resultado"],
                ["1", "GET /api/v1/products/name/teclado"],
                ["2", "Service valida o termo; Repository escapa %, _ e barra invertida"],
                ["3", "SQLite executa LIKE com COLLATE NOCASE"],
                ["4", "API retorna 200, lista e metadado total, inclusive quando a lista é vazia"],
            ],
            [18 * mm, 154 * mm],
        ),
        Spacer(1, 6 * mm),
        p("Mapeamento de exceções", "h2"),
        table(
            [
                ["Origem", "Exceção", "Resposta"],
                ["Model/Zod", "Campo inválido", "422 VALIDATION_ERROR"],
                ["Service", "Produto ausente", "404 NOT_FOUND"],
                ["Service", "Nome duplicado", "409 CONFLICT"],
                ["Router", "Endpoint ausente", "404 ROUTE_NOT_FOUND"],
                ["Infraestrutura", "Erro inesperado", "500 INTERNAL_ERROR sem vazar detalhes"],
            ],
            [48 * mm, 58 * mm, 66 * mm],
        ),
        Spacer(1, 7 * mm),
        callout(
            "Resultado arquitetural",
            "O caminho feliz e as falhas atravessam as mesmas fronteiras bem definidas. Isso reduz duplicação, torna o contrato previsível e permite testar o comportamento completo sem iniciar um processo HTTP externo.",
            PALE_BLUE,
            BLUE,
        ),
        PageBreak(),
    ]

    story += section_title(
        "10",
        "Qualidade, segurança e operação",
        "Mecanismos implementados para tornar a entrega reproduzível e verificável.",
    )
    story += [
        table(
            [
                ["Área", "Mecanismo", "Benefício"],
                ["Validação", "Zod + strict schemas", "Rejeita campos desconhecidos e valores fora do domínio"],
                ["Persistência", "Constraints + índice", "Protege integridade mesmo fora do fluxo HTTP"],
                ["Segurança", "Helmet, CORS, limite 32 KB", "Reduz superfície de configuração insegura"],
                ["Erros", "Envelope e request ID", "Contrato estável e diagnóstico correlacionável"],
                ["Saúde", "GET /health", "Permite health check do contêiner"],
                ["Testes", "Vitest + Supertest", "Verifica API ponta a ponta com banco em memória"],
                ["Entrega", "Docker multi-stage", "Imagem pequena e execução como usuário não root"],
                ["CI", "GitHub Actions", "Executa npm ci e npm test em push e pull request"],
                ["Documentação", "OpenAPI 3.1", "Contrato executável e explorável pelo parceiro"],
            ],
            [30 * mm, 55 * mm, 87 * mm],
        ),
        Spacer(1, 7 * mm),
        p("Cobertura comportamental dos testes", "h2"),
        bullets(
            [
                "Health check e presença do identificador de requisição.",
                "Ciclo completo criar, listar, buscar, contar, atualizar e excluir.",
                "Pesquisa parcial por nome sem diferenciar maiúsculas.",
                "Validação simultânea de nome, preço e estoque.",
                "Conflito de nomes duplicados e padronização de rota inexistente.",
            ]
        ),
        Spacer(1, 7 * mm),
        callout(
            "Evidência de execução",
            "Vitest 5.0.1: 1 arquivo de teste aprovado, 6 testes aprovados e nenhuma falha. A mesma suíte é executada automaticamente pelo workflow de CI.",
        ),
        PageBreak(),
    ]

    story += section_title(
        "11",
        "Execução e demonstração",
        "Passos mínimos para o avaliador reproduzir a solução.",
    )
    story += [
        p("Execução local", "h2"),
        code_block("npm ci\ncp .env.example .env\nnpm run seed\nnpm start"),
        Spacer(1, 6 * mm),
        p("Acessos", "h2"),
        table(
            [
                ["Recurso", "Endereço"],
                ["API", "http://localhost:3000"],
                ["Swagger UI", "http://localhost:3000/docs"],
                ["OpenAPI", "http://localhost:3000/openapi.json"],
                ["Health check", "http://localhost:3000/health"],
            ],
            [48 * mm, 124 * mm],
        ),
        Spacer(1, 6 * mm),
        p("Criação de exemplo", "h2"),
        code_block(
            "curl -X POST http://localhost:3000/api/v1/products \\\n"
            "  -H \"Content-Type: application/json\" \\\n"
            "  -d '{\"name\":\"Notebook Pro 14\",\"price\":5499.90,\"stock\":15}'"
        ),
        Spacer(1, 6 * mm),
        p("Docker e testes", "h2"),
        code_block("docker compose up --build\n\n# Em outro terminal\nnpm test"),
        Spacer(1, 7 * mm),
        callout(
            "Banco de demonstração",
            "O comando npm run seed insere três produtos e é idempotente quanto aos nomes. O banco local fica em data/products.db e não é versionado. O Docker usa um volume persistente.",
            PALE_GOLD,
            colors.HexColor("#D6A73A"),
        ),
        PageBreak(),
    ]

    story += section_title(
        "12",
        "Decisões, limites e evolução",
        "Trade-offs explícitos para demonstrar raciocínio arquitetural além da implementação.",
    )
    story += [
        p("Decisões registradas", "h2"),
        table(
            [
                ["Decisão", "Motivo", "Consequência"],
                ["Node.js + Express", "Aderência ao JavaScript e baixo custo de entrada", "Ecossistema simples e API enxuta"],
                ["SQLite nativo", "Persistência sem serviço externo", "Ótimo para avaliação e pequena escala"],
                ["Service + Repository", "Isolar negócio e infraestrutura", "Mais arquivos, porém melhor evolução e teste"],
                ["OpenAPI no código", "Contrato disponível em runtime", "Mudanças devem acompanhar endpoints"],
                ["UUID gerado na aplicação", "Identificador sem dependência do banco", "Strings maiores que inteiros sequenciais"],
            ],
            [42 * mm, 62 * mm, 68 * mm],
        ),
        Spacer(1, 7 * mm),
        p("Limites conhecidos", "h2"),
        bullets(
            [
                "SQLite prioriza simplicidade e não é a opção final para muitas escritas concorrentes.",
                "A API acadêmica é pública e não implementa autenticação ou autorização por parceiro.",
                "A listagem ainda não possui paginação, filtros combinados ou ordenação selecionável.",
                "Preço usa número decimal em memória; ambiente financeiro crítico deve usar centavos inteiros ou tipo decimal do banco.",
            ]
        ),
        Spacer(1, 7 * mm),
        p("Evolução recomendada", "h2"),
        table(
            [
                ["Fase", "Evolução"],
                ["2", "Autenticação OAuth2/JWT, rate limiting e autorização por escopo"],
                ["3", "PostgreSQL, migrações versionadas e paginação por cursor"],
                ["4", "Logs estruturados, métricas, tracing e SLOs"],
                ["5", "Cache, filas e eventos somente quando carga e casos de uso justificarem"],
            ],
            [20 * mm, 152 * mm],
        ),
        PageBreak(),
    ]

    story += section_title(
        "13",
        "Conclusão e checklist de entrega",
        "Síntese do atendimento ao desafio e localização dos artefatos finais.",
    )
    story += [
        callout(
            "Conclusão",
            "A Partner Products API demonstra os fundamentos solicitados: arquitetura documentada, MVC aplicado, responsabilidades isoladas, contrato REST completo e implementação funcional. Os diferenciais de persistência, testes, documentação executável, Docker e CI tornam a solução verificável e pronta para evolução.",
        ),
        Spacer(1, 8 * mm),
        table(
            [
                ["Entregável", "Arquivo / endereço", "Situação"],
                ["Relatório completo", "docs/entregavel-final-arquitetura-software.pdf", "Pronto"],
                ["Arquitetura em PDF", "docs/diagramas-arquitetura.pdf", "Pronto"],
                ["Arquitetura editável", "docs/arquitetura.drawio", "Pronto"],
                ["Código e documentação", "Repositório GitHub", "Pronto"],
                ["Persistência", "SQLite + seed", "Pronto"],
                ["Testes", "tests/products.e2e.test.js", "6 aprovados"],
            ],
            [48 * mm, 94 * mm, 30 * mm],
        ),
        Spacer(1, 10 * mm),
        p("Repositório do projeto", "h2"),
        callout(
            "Código-fonte e instruções",
            '<link href="https://github.com/ronoellima10-ship-it/desafio-final-arquiteto-software-api" color="#176B87"><b>github.com/ronoellima10-ship-it/desafio-final-arquiteto-software-api</b></link><br/>O README contém instalação, endpoints, exemplos, testes e links para todos os entregáveis.',
            PALE_BLUE,
            BLUE,
        ),
        Spacer(1, 12 * mm),
        p("<b>Autor:</b> Ronoel Lima<br/><b>Data:</b> 19 de setembro de 2026<br/><b>Projeto:</b> Desafio Final - Bootcamp Arquiteto(a) de Software"),
    ]

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)


def diagram_page(canvas, image_path, title, subtitle, page_number):
    width, height = landscape(A4)
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, width, height, stroke=0, fill=1)
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 14 * mm, width, 14 * mm, stroke=0, fill=1)
    canvas.setFont("DejaVu-Bold", 15)
    canvas.setFillColor(WHITE)
    canvas.drawString(15 * mm, height - 9.2 * mm, title)
    canvas.setFont("DejaVu", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(15 * mm, height - 20 * mm, subtitle)

    image = Image(str(image_path))
    max_width = width - 26 * mm
    max_height = height - 39 * mm
    ratio = min(max_width / image.imageWidth, max_height / image.imageHeight)
    draw_width = image.imageWidth * ratio
    draw_height = image.imageHeight * ratio
    image.drawWidth = draw_width
    image.drawHeight = draw_height
    image.wrapOn(canvas, draw_width, draw_height)
    image.drawOn(canvas, (width - draw_width) / 2, 14 * mm)

    canvas.setStrokeColor(LINE)
    canvas.line(15 * mm, 9 * mm, width - 15 * mm, 9 * mm)
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(15 * mm, 4.5 * mm, "Arquivo editável: docs/arquitetura.drawio")
    canvas.drawRightString(width - 15 * mm, 4.5 * mm, f"Diagrama {page_number} de 2")
    canvas.showPage()


def build_diagrams_pdf():
    from reportlab.pdfgen import canvas as canvas_module

    c4_png = TMP / "c4-conteineres.png"
    mvc_png = TMP / "mvc-componentes.png"
    canvas = canvas_module.Canvas(
        str(DIAGRAMS_PATH),
        pagesize=landscape(A4),
        pageCompression=1,
    )
    canvas.setTitle("Diagramas da Arquitetura - Partner Products API")
    canvas.setAuthor("Ronoel Lima")
    diagram_page(
        canvas,
        c4_png,
        "Partner Products API - C4 Nível 2",
        "Visão de contêineres, integrações e responsabilidades em tempo de execução.",
        1,
    )
    diagram_page(
        canvas,
        mvc_png,
        "Partner Products API - Componentes MVC",
        "Fluxo da requisição e separação entre interface, negócio, validação e persistência.",
        2,
    )
    canvas.save()


if __name__ == "__main__":
    build_diagrams_pdf()
    build_report()
    print(REPORT_PATH)
    print(DIAGRAMS_PATH)
