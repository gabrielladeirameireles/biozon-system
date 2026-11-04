from fastapi import APIRouter, Request, Depends, Form, HTTPException, status, responses, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from urllib.parse import quote
import io

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.database import get_db
from app.models import ServiceOrder, AdminUser
from app.auth import verify_password, get_current_user_from_session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def require_admin(request: Request):
    user = get_current_user_from_session(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/admin/login"}
        )
    return user

def clean_float_input(value: str) -> float:
    if not value:
        return 0.0
    val_str = str(value).strip().replace("R$", "").strip()
    if "," in val_str and "." in val_str:
        val_str = val_str.replace(".", "").replace(",", ".")
    elif "," in val_str:
        val_str = val_str.replace(",", ".")
    try:
        return float(val_str)
    except ValueError:
        return 0.0

# ==========================================
# GERADOR DE PDF PROFISSIONAL (REPORTLAB)
# ==========================================

def generate_os_pdf_bytes(order: ServiceOrder) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    PRIMARY = colors.HexColor("#0284c7")
    DARK_TEXT = colors.HexColor("#0f172a")
    MUTED_TEXT = colors.HexColor("#475569")
    LIGHT_BG = colors.HexColor("#f0f9ff")
    BORDER_COLOR = colors.HexColor("#bae6fd")
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=PRIMARY)
    h2_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=PRIMARY, spaceAfter=6)
    body_bold = ParagraphStyle('BodyBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=DARK_TEXT)
    body_normal = ParagraphStyle('BodyNormal', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=DARK_TEXT)

    elements = []
    created_str = order.created_at.strftime("%d/%m/%Y") if order.created_at else datetime.now().strftime("%d/%m/%Y")
    
    header_data = [
        [
            Paragraph("<b>BIOZON PURIFICADORES</b><br/><font size=8 color='#64748b'>Assistência Técnica Autorizada Hidrofiltros - Fortaleza/CE</font>", title_style),
            Paragraph(f"<font size=11 color='#0284c7'><b>COMPROVANTE DE SERVIÇO</b></font><br/><font size=9 color='#0f172a'><b>OS #{order.id:04d}</b></font><br/><font size=8 color='#64748b'>Emissão: {created_str}</font>", ParagraphStyle('RightHeader', parent=styles['Normal'], alignment=2))
        ]
    ]
    header_table = Table(header_data, colWidths=[320, 200])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8)
    ]))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceBefore=4, spaceAfter=14))

    elements.append(Paragraph("DADOS DO CLIENTE & LOCALIZAÇÃO", h2_style))
    client_info = [
        [Paragraph("<b>Cliente:</b>", body_bold), Paragraph(order.client_name or "", body_normal), Paragraph("<b>Telefone:</b>", body_bold), Paragraph(order.client_phone or "", body_normal)],
        [Paragraph("<b>Bairro:</b>", body_bold), Paragraph(order.neighborhood or "", body_normal), Paragraph("<b>Endereço:</b>", body_bold), Paragraph(order.address or "", body_normal)]
    ]
    client_table = Table(client_info, colWidths=[65, 195, 65, 195])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    elements.append(client_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("DETALHAMENTO DO SERVIÇO & FINANCEIRO", h2_style))
    val_parts = order.value_parts or 0.0
    val_labor = order.value_labor or 0.0
    tot_val = order.total_value or 0.0
    
    service_info = [
        [Paragraph("<b>Equipamento:</b>", body_bold), Paragraph(order.equipment or "", body_normal), Paragraph("<b>Serviço:</b>", body_bold), Paragraph(order.service_type or "Geral", body_normal)],
        [Paragraph("<b>Valor Peças/Refil:</b>", body_bold), Paragraph(f"R$ {val_parts:.2f}", body_normal), Paragraph("<b>Mão de Obra:</b>", body_bold), Paragraph(f"R$ {val_labor:.2f}", body_normal)],
        [Paragraph("<b>Forma de Pagto:</b>", body_bold), Paragraph(order.payment_method or "Pix", body_normal), Paragraph("<b>Nota Fiscal:</b>", body_bold), Paragraph(order.invoice_number or "N/I", body_normal)],
        [Paragraph("<b>VALOR TOTAL:</b>", body_bold), Paragraph(f"<b>R$ {tot_val:.2f}</b>", body_normal), Paragraph("<b>Status:</b>", body_bold), Paragraph(f"<b>{order.status or 'Pendente'}</b>", body_normal)]
    ]
    if order.notes:
        service_info.append([
            Paragraph("<b>Observações:</b>", body_bold),
            Paragraph(order.notes, body_normal),
            Paragraph("", body_normal),
            Paragraph("", body_normal)
        ])

    service_table = Table(service_info, colWidths=[100, 160, 100, 160])
    service_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    elements.append(service_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("PROGRAMAÇÃO DE RECORRÊNCIA (180 DIAS)", h2_style))
    next_date = order.next_maintenance_date or "Em 6 meses"
    maint_box = [[Paragraph(f"<font size=10 color='#0369a1'><b>PRÓXIMA TROCA RECOMENDADA: {next_date}</b></font><br/><font size=8 color='#334155'>Substituição preventiva do elemento filtrante para garantir a pureza da água. A BIOZON entrará em contato para agendamento.</font>", ParagraphStyle('Maint', parent=styles['Normal'], leading=12))]]
    maint_table = Table(maint_box, colWidths=[520])
    maint_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1.5, PRIMARY),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    elements.append(maint_table)
    elements.append(Spacer(1, 24))

    sig_data = [[
        Paragraph("__________________________________________<br/><b>BIOZON Purificadores</b><br/><font size=8>Getúlio Ladeira - Téc. Responsável</font>", ParagraphStyle('Sig1', parent=styles['Normal'], alignment=1, fontSize=8)),
        Paragraph("__________________________________________<br/><b>Assinatura do Cliente</b><br/><font size=8>Aceite dos Serviços Prestados</font>", ParagraphStyle('Sig2', parent=styles['Normal'], alignment=1, fontSize=8))
    ]]
    sig_table = Table(sig_data, colWidths=[260, 260])
    elements.append(sig_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# ==========================================
# ROTAS DO PAINEL ADMIN
# ==========================================

@router.get("/admin/login")
def login_page(request: Request):
    if get_current_user_from_session(request):
        return responses.RedirectResponse(url="/admin/os", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request=request, name="admin/login.html", context={"error": None})

@router.post("/admin/login")
def login_action(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(request=request, name="admin/login.html", context={"error": "Usuário ou senha incorretos."}, status_code=status.HTTP_400_BAD_REQUEST)
    request.session["user"] = user.username
    return responses.RedirectResponse(url="/admin/os", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/logout")
def logout(request: Request):
    request.session.clear()
    return responses.RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/os")
def list_os(request: Request, status_filter: str = None, neighborhood_filter: str = None, db: Session = Depends(get_db), user: str = Depends(require_admin)):
    query = db.query(ServiceOrder)
    if status_filter:
        query = query.filter(ServiceOrder.status == status_filter)
    if neighborhood_filter:
        query = query.filter(ServiceOrder.neighborhood.ilike(f"%{neighborhood_filter}%"))
    orders = query.order_by(ServiceOrder.created_at.desc()).all()
    return templates.TemplateResponse(request=request, name="admin/os_list.html", context={"orders": orders, "status_filter": status_filter or "", "neighborhood_filter": neighborhood_filter or "", "current_user": user})

@router.post("/admin/os/new")
def create_service_order(
    request: Request,
    client_name: str = Form(...),
    client_phone: str = Form(...),
    neighborhood: str = Form(...),
    address: str = Form(...),
    equipment: str = Form(...),
    service_type: str = Form(...),
    value_parts: str = Form("0"),
    value_labor: str = Form("0"),
    payment_method: str = Form("Pix"),
    invoice_number: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
    user: str = Depends(require_admin)
):
    parts_val = clean_float_input(value_parts)
    labor_val = clean_float_input(value_labor)
    clean_phone = "".join(filter(str.isdigit, client_phone))
    total_val = parts_val + labor_val
    next_maint = (datetime.utcnow() + timedelta(days=180)).strftime("%d/%m/%Y")
    
    new_order = ServiceOrder(
        client_name=client_name,
        client_phone=clean_phone,
        neighborhood=neighborhood,
        address=address,
        equipment=equipment,
        service_type=service_type,
        value_parts=parts_val,
        value_labor=labor_val,
        total_value=total_val,
        payment_method=payment_method,
        invoice_number=invoice_number,
        notes=notes,
        status="Pendente",
        next_maintenance_date=next_maint
    )
    db.add(new_order)
    db.commit()
    return responses.RedirectResponse(url="/admin/os", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/os/{order_id}/pdf")
def get_service_order_pdf(order_id: int, db: Session = Depends(get_db), user: str = Depends(require_admin)):
    order = db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="OS não encontrada.")
    
    pdf_bytes = generate_os_pdf_bytes(order)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=comprovante_BIOZON_OS_{order.id:04d}.pdf"}
    )

@router.post("/admin/os/{order_id}/status")
def update_service_order_status(order_id: int, new_status: str = Form(...), db: Session = Depends(get_db), user: str = Depends(require_admin)):
    order = db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
    if order:
        order.status = new_status
        if new_status == "Concluído":
            order.next_maintenance_date = (datetime.utcnow() + timedelta(days=180)).strftime("%d/%m/%Y")
        db.commit()
    return responses.RedirectResponse(url="/admin/os", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/clients/{phone}")
def client_detail(phone: str, request: Request, db: Session = Depends(get_db), user: str = Depends(require_admin)):
    orders = db.query(ServiceOrder).filter(ServiceOrder.client_phone == phone).order_by(ServiceOrder.created_at.desc()).all()
    if not orders:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    client_info = {"name": orders[0].client_name, "phone": orders[0].client_phone, "neighborhood": orders[0].neighborhood, "address": orders[0].address, "total_services": len(orders)}
    return templates.TemplateResponse(request=request, name="admin/client_detail.html", context={"client": client_info, "orders": orders, "current_user": user})

@router.get("/admin/maintenance/due")
def maintenance_due_list(request: Request, db: Session = Depends(get_db), user: str = Depends(require_admin)):
    date_180_days_ago = datetime.utcnow() - timedelta(days=180)
    pending_refill_orders = db.query(ServiceOrder).filter(ServiceOrder.status == "Concluído", ServiceOrder.updated_at <= date_180_days_ago).order_by(ServiceOrder.updated_at.asc()).all()
    for order in pending_refill_orders:
        clean_phone = "".join(filter(str.isdigit, order.client_phone or ""))
        if not clean_phone.startswith("55"):
            clean_phone = f"55{clean_phone}"
        msg = f"Olá, {order.client_name}! Aqui é Getúlio da BIOZON. A última troca de refil do seu purificador completou 6 meses. Podemos agendar a troca preventiva?"
        order.wa_link = f"https://wa.me/{clean_phone}?text={quote(msg)}"
    return templates.TemplateResponse(request=request, name="admin/maintenance_due.html", context={"orders": pending_refill_orders, "current_user": user})
