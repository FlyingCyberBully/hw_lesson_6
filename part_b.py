from part_a import (
    get_correct_email,
    check_empty_fields,
    clean_body_text,
    normalize_addresses,
    create_email,
    add_send_date,
    extract_login_domain,
    mask_sender_email,
    add_short_body,
    build_sent_text,
)


def sender_email(
    recipient_list: list[str],
    subject: str,
    message: str,
    *,
    sender="default@study.com"
) -> list[dict]:
    """
    Полная обработка писем согласно заданию.
    """

    if not recipient_list:
        return []

    # 1. Проверка корректности адресов
    valid_recipients = get_correct_email(recipient_list)
    valid_sender = get_correct_email([sender])

    if not valid_sender or not valid_recipients:
        return []

    sender = valid_sender[0]

    # 2. Проверка пустоты темы/тела
    is_sub_empty, is_body_empty = check_empty_fields(subject, message)
    if is_sub_empty or is_body_empty:
        return []

    # 3. Исключить отправку самому себе
    valid_recipients = [r for r in valid_recipients if r != sender]
    if not valid_recipients:
        return []

    # 4. Очистка текста
    subject = clean_body_text(subject)
    message = clean_body_text(message)

    # 5. Нормализация email
    recipient_list = [normalize_addresses(r) for r in valid_recipients]
    sender = normalize_addresses(sender)

    # 6. Создание структуры писем
    emails = [
        create_email(sender, recipient, subject, message)
        for recipient in recipient_list
    ]

    result = []

    for email in emails:
        add_send_date(email)

        # маска отправителя
        login, domain = extract_login_domain(email["sender"])
        email["masked_sender"] = mask_sender_email(login, domain)

        # короткое тело
        add_short_body(email)

        # итоговый текст
        email["sent_text"] = build_sent_text(email)

        result.append(email)

    return result


emails = sender_email(
    ["admin@company.ru", " hello@corp.ru  "],
    subject="Hello!",
    message="Привет, коллега!",
)

for e in emails:
    print(e, "\n")