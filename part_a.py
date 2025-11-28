from datetime import date
from typing import Tuple, List, Dict


def normalize_addresses(value: str) -> str:
    """
    Возвращает строку, приведённую к нижнему регистру
    и очищенную от пробелов по краям.
    """
    if not isinstance(value, str):
        return ""
    return value.strip().lower()


def add_short_body(email: Dict) -> Dict:
    """
    Добавляет email["short_body"] = первые 10 символов тела + "..."
    """
    body = email.get("body", "")
    email["short_body"] = body[:10] + "..." if len(body) > 10 else body
    return email


def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    if not isinstance(body, str):
        return ""
    return body.replace("\n", " ").replace("\t", " ")


def build_sent_text(email: Dict) -> str:
    """
    Формирует итоговый текст письма.
    """
    return (
        f"Кому: {email['recipient']}, от {email['sender']}\n"
        f"Тема: {email['subject']}, дата {email['date']}\n"
        f"{email['short_body']}"
    )


def check_empty_fields(subject: str, body: str) -> Tuple[bool, bool]:
    """
    Возвращает (is_subject_empty, is_body_empty)
    """
    subject = subject or ""
    body = body or ""

    return (not subject.strip(), not body.strip())


def mask_sender_email(login: str, domain: str) -> str:
    """
    Маскирует email: первые 2 символа логина + "***@" + домен.
    """
    login = login or ""
    return f"{login[:2]}***@{domain}"


def get_correct_email(email_list: List[str]) -> List[str]:
    """
    Возвращает список корректных email.
    """
    valid_domains = (".com", ".ru", ".net")
    result = []

    for email in email_list:
        clean = normalize_addresses(email)
        if "@" not in clean:
            continue
        if not clean.endswith(valid_domains):
            continue
        result.append(clean)

    return result


def create_email(sender: str, recipient: str, subject: str, body: str) -> Dict:
    """
    Создаёт структуру письма.
    """
    return {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body,
    }


def add_send_date(email: Dict) -> Dict:
    """
    Добавляет текущую дату YYYY-MM-DD.
    """
    email["date"] = date.today().isoformat()
    return email


def extract_login_domain(address: str) -> Tuple[str, str]:
    """
    Возвращает логин и домен email.
    """
    if "@" not in address:
        return "", ""
    login, domain = address.split("@", 1)
    return login, domain
