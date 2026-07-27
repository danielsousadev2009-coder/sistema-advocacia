"""
Geração do PDF "Ficha do Cliente" (RF - PDF Automático).

Monta um documento PDF com os dados cadastrais do cliente, cabeçalho
com o nome do escritório e rodapé com data/hora de emissão. Usa
reportlab (Platypus) para o layout.
"""

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


def _formatar_data(dt):
    if not dt:
        return "-"
    return dt.strftime("%d/%m/%Y às %H:%M")


def _label_tipo_pessoa(tipo_pessoa):
    return "Pessoa física" if tipo_pessoa == "fisica" else "Pessoa jurídica"


def gerar_pdf_ficha_cliente(cliente):
    """
    Recebe uma instância de clientes.models.Cliente e retorna um
    buffer (io.BytesIO) com o PDF gerado, pronto para ser enviado
    numa HttpResponse/FileResponse.
    """
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        title=f"Ficha do Cliente - {cliente.nome}",
    )

    styles = getSampleStyleSheet()

    titulo_escritorio_style = ParagraphStyle(
        "TituloEscritorio",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=2,
    )
    subtitulo_style = ParagraphStyle(
        "Subtitulo",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#555555"),
        spaceAfter=12,
    )
    titulo_ficha_style = ParagraphStyle(
        "TituloFicha",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#1a1a1a"),
        spaceBefore=10,
        spaceAfter=10,
    )
    rodape_style = ParagraphStyle(
        "Rodape",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#888888"),
    )

    story = []

    escritorio = cliente.escritorio
    nome_escritorio = getattr(escritorio, "nome", None) or str(escritorio)

    story.append(Paragraph(nome_escritorio, titulo_escritorio_style))
    story.append(Paragraph("Sistema de Gestão para Escritórios de Advocacia", subtitulo_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Ficha do Cliente", titulo_ficha_style))

    status_label = "Ativo" if cliente.ativo else "Inativo"

    dados = [
        ["Nome", cliente.nome],
        ["Tipo de pessoa", _label_tipo_pessoa(cliente.tipo_pessoa)],
        ["CPF/CNPJ", cliente.cpf_cnpj or "-"],
        ["E-mail", cliente.email or "-"],
        ["Telefone", cliente.telefone or "-"],
        ["Endereço", cliente.endereco or "-"],
        ["Status", status_label],
        ["Cliente desde", _formatar_data(cliente.criado_em)],
    ]

    tabela = Table(dados, colWidths=[4.5 * cm, 10.5 * cm])
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f2f2f2")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#333333")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(tabela)

    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd")))
    story.append(Spacer(1, 6))
    story.append(
        Paragraph(
            f"Documento gerado automaticamente em {_formatar_data(datetime.now())}.",
            rodape_style,
        )
    )

    doc.build(story)

    buffer.seek(0)
    return buffer