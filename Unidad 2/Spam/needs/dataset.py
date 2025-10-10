from typing import List
from needs.email import Email


# =========================================================
# 3) Dataset de ejemplo + demo __main__
# =========================================================
EXAMPLE_DATASET: List[Email] = [
    Email(
        subject="¡FELICITACIONES! Gana dinero rápido desde casa",
        sender="promo@cheapoffers.biz",
        body="Gana dinero rápido sin esfuerzo. Haz clic en https://bit.ly/xyz para obtener tu premio GRATIS.",
        attachments=[],
        label="spam",
    ),
    Email(
        subject="Reunión de proyecto – acta y acuerdos",
        sender="jefa@miempresa.com",
        body="Hola equipo, adjunto el acta en PDF y el enlace a la minuta.",
        attachments=["acta-proyecto.pdf"],
        label="ham",
    ),
    Email(
        subject="URGENTE: Verifica tu cuenta ahora!!!",
        sender="support@winner-prize.ru",
        body="Tu cuenta será suspendida. Verifica en https://verify-acc.mov/login",
        attachments=[],
        label="spam",
    ),
    Email(
        subject="Boletín mensual de la comunidad",
        sender="hola@comunidad.mx",
        body="Gracias por participar. Aquí nuestras próximas actividades y un artículo sobre seguridad digital.",
        attachments=[],
        label="ham",
    ),
    Email(
        subject="Oferta EXCLUSIVA solo hoy",
        sender="ventas@quick-rich.cn",
        body="Última oportunidad: promoción 2x1. Más info en https://tinyurl.com/ahorro-2025",
        attachments=[],
        label="spam",
    ),
    Email(
        subject="Factura de servicios septiembre",
        sender="facturacion@utilidades.com",
        body="Estimado cliente, su factura está disponible en el portal. Saludos.",
        attachments=["factura-0925.xml", "factura-0925.pdf"],
        label="ham",
    ),
    Email(
        subject="Actualiza tu CV para esta vacante remota",
        sender="reclutamiento@empleos.co",
        body="Tenemos roles remotos legítimos. Aplica aquí: https://empleos.co/oferta/123",
        attachments=[],
        label="ham",
    ),
    Email(
        subject="Regalo para ti – descarga",
        sender="no-reply@spam-now.top",
        body="Descarga el mejor regalo aquí: https://free-gift.top y abre el adjunto",
        attachments=["setup_gift.exe"],
        label="spam",
    ),
]
