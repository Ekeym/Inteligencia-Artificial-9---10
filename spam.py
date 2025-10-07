# spam_rules_demo.py
from __future__ import annotations
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Iterable
from collections import Counter

# ---------------------------
# 1) Representación del correo
# ---------------------------
@dataclass
class Email:
    subject: str
    sender: str
    body: str
    attachments: List[str]
    label: str

    def urls(self) -> List[str]:
        url_regex = r"(https?://[^\s]+)"
        return re.findall(url_regex, self.body, flags=re.I)

# --------------------------------
# 2) Conjunto de reglas y utilidades
# --------------------------------
SUSPICIOUS_KEYWORDS = {
    "dinero rápido", "gana dinero", "trabajo desde casa", "gratis", "urgente",
    "haz clic", "oferta", "promoción", "felicitaciones", "bitcoins", "crédito",
    "viagra", "premio", "regalo", "aumenta tus ingresos"
}

DANGEROUS_EXTENSIONS = {".exe", ".bat", ".js", ".vbs", ".scr", ".jar"}

BAD_SENDER_DOMAINS = {
    "cheapoffers.biz", "winner-prize.ru", "quick-rich.cn", "spam-now.top"
}

URL_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly"}

SUSPICIOUS_TLDS = {".ru", ".cn", ".work", ".top", ".zip", ".mov"}

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def domain_of(email_address: str) -> str:
    m = re.search(r"@([^> )]+)$", email_address)
    return (m.group(1) if m else "").lower()

def has_dangerous_attachment(attachments: Iterable[str]) -> bool:
    for name in attachments:
        name = name.lower().strip()
        for ext in DANGEROUS_EXTENSIONS:
            if name.endswith(ext):
                return True
    return False

def keyword_hits(text: str, keywords: Iterable[str]) -> int:
    t = normalize(text)
    hits = 0
    for kw in keywords:
        if kw in t:
            hits += 1
    return hits

def url_domain(url: str) -> str:
    
    m = re.match(r"https?://([^/]+)/?", url, flags=re.I)
    return m.group(1).lower() if m else ""

def looks_like_suspicious_url(url: str) -> bool:
    d = url_domain(url)
    
    if d in URL_SHORTENERS:
        return True
    
    for tld in SUSPICIOUS_TLDS:
        if d.endswith(tld):
            return True
        
    if re.search(r"[0-9].*[0-9]", d) and "-" in d:
        return True
    return False

# -----------------------------
# 3) Motor de scoring por reglas
# -----------------------------
RuleScore = Dict[str, float]

DEFAULT_WEIGHTS: RuleScore = {
    "kw_subject": 2.0,
    "kw_body": 1.5, 
    "sender_bad_domain": 3.0,
    "dangerous_attachment": 4.0,
    "suspicious_url": 2.0,
    "many_urls": 1.0,
    "all_caps_subject": 1.0,
    "urgency_subject": 1.0,
}

URGENCY_WORDS = {"urgente", "ahora", "última oportunidad", "solo hoy"}

def spam_score(email: Email, weights: RuleScore = DEFAULT_WEIGHTS) -> Tuple[float, Dict[str, float]]:
    reasons: Dict[str, float] = {}
    subject = email.subject or ""
    body = email.body or ""

    sub_hits = keyword_hits(subject, SUSPICIOUS_KEYWORDS)
    if sub_hits:
        reasons["kw_subject"] = sub_hits * weights["kw_subject"]

    body_hits = keyword_hits(body, SUSPICIOUS_KEYWORDS)
    if body_hits:
        reasons["kw_body"] = min(body_hits, 4) * weights["kw_body"]

    dom = domain_of(email.sender)
    if dom in BAD_SENDER_DOMAINS:
        reasons["sender_bad_domain"] = weights["sender_bad_domain"]

    if has_dangerous_attachment(email.attachments):
        reasons["dangerous_attachment"] = weights["dangerous_attachment"]

    urls = email.urls()
    sus_urls = sum(looks_like_suspicious_url(u) for u in urls)
    if sus_urls:
        reasons["suspicious_url"] = min(sus_urls, 3) * weights["suspicious_url"]
    if len(urls) >= 3:
        reasons["many_urls"] = weights["many_urls"]

    if subject.isupper() and len(subject) >= 6:
        reasons["all_caps_subject"] = weights["all_caps_subject"]
    if keyword_hits(subject, URGENCY_WORDS) or "!!!" in subject:
        reasons["urgency_subject"] = weights["urgency_subject"]

    total = sum(reasons.values())
    return total, reasons

def classify(email: Email, threshold: float = 3.0) -> Tuple[str, float, Dict[str, float]]:
    score, reasons = spam_score(email)
    label = "spam" if score >= threshold else "ham"
    return label, score, reasons

# -----------------------------------------
# 4) Dataset de ejemplo + evaluación rápida
# -----------------------------------------
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

def evaluate(dataset: List[Email], threshold: float = 3.0) -> None:
    y_true, y_pred = [], []
    details = []
    for e in dataset:
        pred, score, reasons = classify(e, threshold)
        y_true.append(e.label)
        y_pred.append(pred)
        details.append((e.subject, e.label, pred, score, reasons))

    def metrics(y_true, y_pred, positive="spam") -> Dict[str, float]:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == positive and p == positive)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != positive and p == positive)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == positive and p != positive)
        tn = sum(1 for t, p in zip(y_true, y_pred) if t != positive and p != positive)
        acc = (tp + tn) / max(len(y_true), 1)
        prec = tp / max(tp + fp, 1)
        rec = tp / max(tp + fn, 1)
        f1 = (2 * prec * rec) / max(prec + rec, 1e-9)
        return {"acc": acc, "precision": prec, "recall": rec, "f1": f1, "cm": (tp, fp, fn, tn)}

    m = metrics(y_true, y_pred, positive="spam")
    print("\n=== RESULTADOS (umbral={}) ===".format(threshold))
    print("Accuracy:  {acc:.3f}  Precision: {precision:.3f}  Recall: {recall:.3f}  F1: {f1:.3f}".format(**m))
    tp, fp, fn, tn = m["cm"]
    print("Matriz de confusión  (spam=positivo):")
    print(f"  TP={tp}  FP={fp}  FN={fn}  TN={tn}\n")

    print("— Ejemplos y razones —")
    for subj, y, p, sc, r in details:
        print(f"[{y} -> {p}] score={sc:.1f} | {subj}")
        if r:
            for k, v in sorted(r.items(), key=lambda kv: -kv[1]):
                print(f"   - {k}: +{v:.1f}")
        else:
            print("   - (sin señales de spam)")
        print()

if __name__ == "__main__":
    evaluate(EXAMPLE_DATASET, threshold=3.0)