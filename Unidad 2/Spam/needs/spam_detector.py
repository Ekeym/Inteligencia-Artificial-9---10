from typing import List, Dict, Tuple, Iterable
from needs.email import Email 
import re

# =========================================================
# 2) Verificador OO: reglas, scoring y evaluación
# =========================================================

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
DEFAULT_SUSPICIOUS_KEYWORDS = {
    "dinero rápido", "gana dinero", "trabajo desde casa", "gratis", "urgente",
    "haz clic", "oferta", "promoción", "felicitaciones", "bitcoins", "crédito",
    "viagra", "premio", "regalo", "aumenta tus ingresos"
}
DEFAULT_DANGEROUS_EXTENSIONS = {".exe", ".bat", ".js", ".vbs", ".scr", ".jar"}
DEFAULT_BAD_SENDER_DOMAINS = {
    "cheapoffers.biz", "winner-prize.ru", "quick-rich.cn", "spam-now.top"
}
DEFAULT_URL_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly"}
DEFAULT_SUSPICIOUS_TLDS = {".ru", ".cn", ".work", ".top", ".zip", ".mov"}
DEFAULT_URGENCY_WORDS = {"urgente", "ahora", "última oportunidad", "solo hoy"}

class SpamVerifier:

    def __init__(
        self,
        *,
        suspicious_keywords: Iterable[str] = DEFAULT_SUSPICIOUS_KEYWORDS,
        dangerous_extensions: Iterable[str] = DEFAULT_DANGEROUS_EXTENSIONS,
        bad_sender_domains: Iterable[str] = DEFAULT_BAD_SENDER_DOMAINS,
        url_shorteners: Iterable[str] = DEFAULT_URL_SHORTENERS,
        suspicious_tlds: Iterable[str] = DEFAULT_SUSPICIOUS_TLDS,
        urgency_words: Iterable[str] = DEFAULT_URGENCY_WORDS,
        weights: RuleScore = None,
        threshold: float = 3.0,
        max_kw_body_multiplicity: int = 4,
        max_suspicious_urls_multiplicity: int = 3,
        many_urls_cutoff: int = 3,
    ) -> None:
        self.suspicious_keywords = set(suspicious_keywords)
        self.dangerous_extensions = set(dangerous_extensions)
        self.bad_sender_domains = set(bad_sender_domains)
        self.url_shorteners = set(url_shorteners)
        self.suspicious_tlds = set(suspicious_tlds)
        self.urgency_words = set(urgency_words)
        self.weights: RuleScore = dict(DEFAULT_WEIGHTS if weights is None else weights)
        self.threshold = threshold

        # Parámetros reglas
        self.max_kw_body_multiplicity = max_kw_body_multiplicity
        self.max_suspicious_urls_multiplicity = max_suspicious_urls_multiplicity
        self.many_urls_cutoff = many_urls_cutoff

    # ------------------------
    # Utilidades internas
    # ------------------------
    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", (text or "").lower()).strip()

    @staticmethod
    def _domain_of(email_address: str) -> str:
        result_regex = re.search(r"@([^> )]+)$", email_address or "")
        return (result_regex.group(1) if result_regex else "").lower()

    @staticmethod
    def _url_domain(url: str) -> str:
        result_regex = re.match(r"https?://([^/]+)/?", url or "", flags=re.I)
        return result_regex.group(1).lower() if result_regex else ""

    def _has_dangerous_attachment(self, attachments: Iterable[str]) -> bool:
        for name in attachments or []:
            name = (name or "").lower().strip()
            for ext in self.dangerous_extensions:
                if name.endswith(ext):
                    return True
        return False

    def _keyword_hits(self, text: str, keywords: Iterable[str]) -> int:
        t = self._normalize(text)
        return sum(1 for kw in keywords if kw in t)

    def _looks_like_suspicious_url(self, url: str) -> bool:
        sample = self._url_domain(url)

        if not sample:
            return False

        # Acortadores
        if sample in self.url_shorteners:
            return True

        # TLDs sospechosos
        for tld in self.suspicious_tlds:
            if sample.endswith(tld):
                return True

        # Heurística de dominio “ruidoso”
        if re.search(r"[0-9].*[0-9]", sample) and "-" in sample:
            return True

        return False

    # ------------------------
    # Scoring y clasificación
    # ------------------------
    def score(self, email: Email) -> Tuple[float, Dict[str, float]]:
        reasons: Dict[str, float] = {}
        subject = email.subject or ""
        body = email.body or ""

        # Palabras sospechosas
        sub_hits = self._keyword_hits(subject, self.suspicious_keywords)
        if sub_hits:
            reasons["kw_subject"] = sub_hits * self.weights["kw_subject"]

        body_hits = self._keyword_hits(body, self.suspicious_keywords)
        if body_hits:
            reasons["kw_body"] = min(body_hits, self.max_kw_body_multiplicity) * self.weights["kw_body"]

        # Dominio del remitente
        dom = self._domain_of(email.sender)
        if dom in self.bad_sender_domains:
            reasons["sender_bad_domain"] = self.weights["sender_bad_domain"]

        # Adjuntos peligrosos
        if self._has_dangerous_attachment(email.attachments):
            reasons["dangerous_attachment"] = self.weights["dangerous_attachment"]

        # URLs sospechosas / muchas URLs
        urls = email.urls()
        sus_urls = sum(1 for u in urls if self._looks_like_suspicious_url(u))
        if sus_urls:
            reasons["suspicious_url"] = min(sus_urls, self.max_suspicious_urls_multiplicity) * self.weights["suspicious_url"]
        if len(urls) >= self.many_urls_cutoff:
            reasons["many_urls"] = self.weights["many_urls"]

        # Gritos y urgencia
        if subject.isupper() and len(subject) >= 6:
            reasons["all_caps_subject"] = self.weights["all_caps_subject"]
        if self._keyword_hits(subject, self.urgency_words) or "!!!" in subject:
            reasons["urgency_subject"] = self.weights["urgency_subject"]

        return sum(reasons.values()), reasons

    def classify(self, email: Email) -> Tuple[str, float, Dict[str, float]]:
        score, reasons = self.score(email)
        label = "spam" if score >= self.threshold else "ham"
        return label, score, reasons

    # ------------------------
    # Evaluación rápida
    # ------------------------
    @staticmethod
    def _metrics(y_true: List[str], y_pred: List[str], positive: str = "spam") -> Dict[str, float | Tuple[int, int, int, int]]:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == positive and p == positive)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != positive and p == positive)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == positive and p != positive)
        tn = sum(1 for t, p in zip(y_true, y_pred) if t != positive and p != positive)
        acc = (tp + tn) / max(len(y_true), 1)
        prec = tp / max(tp + fp, 1)
        rec = tp / max(tp + fn, 1)
        f1 = (2 * prec * rec) / max(prec + rec, 1e-9)
        return {"acc": acc, "precision": prec, "recall": rec, "f1": f1, "cm": (tp, fp, fn, tn)}

    def evaluate(self, dataset: List[Email]) -> None:
        y_true, y_pred = [], []
        details = []
        for e in dataset:
            pred, score, reasons = self.classify(e)
            y_true.append(e.label or "ham")
            y_pred.append(pred)
            details.append((e.subject, e.label or "ham", pred, score, reasons))

        m = self._metrics(y_true, y_pred, positive="spam")
        print("\n————— RESULTADOS —————")
        print("Accuracy:  {acc:.3f}  Precision: {precision:.3f}  Recall: {recall:.3f}  F1: {f1:.3f}".format(**m))
        tp, fp, fn, tn = m["cm"]
        print("Matriz de confusión  (spam=positivo):")
        print(f"  TP={tp}  FP={fp}  FN={fn}  TN={tn}\n")

        print("————— Ejemplos —————")
        for subj, y, p, sc, r in details:
            print(f"[{y} -> {p}] score={sc:.1f} | {subj}")
            if r:
                for k, v in sorted(r.items(), key=lambda kv: -kv[1]):
                    print(f"   - {k}: +{v:.1f}")
            else:
                print("————— Sin Spam —————")
            print()
