#!/usr/bin/env python3
"""Генератор сайта notriplea.com: политики конфиденциальности всех игр (EN + RU).

Запуск из корня репозитория:  python3 tools/build.py
Настройки игр — tools/games.json. Текст политики — здесь, в TEXT.
Перезаписывает index.html и <slug>/privacy/index.html, <slug>/privacy/ru/index.html.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "tools", "games.json"), encoding="utf-8"))
EMAIL = CFG["email"]


def mail():
    return f'<a href="mailto:{EMAIL}">{EMAIL}</a>'


# ---------------------------------------------------------------- тексты

def text_en(g):
    name = html.escape(g["name"])
    nets = ["Google AdMob", "Unity Ads"] + (["Yandex Ads"] if g["yandexAds"] else [])
    nets_html = ", ".join(f"<strong>{n}</strong>" for n in nets[:-1]) + f" and <strong>{nets[-1]}</strong>"
    s = []
    s.append(f"""<div class="card">
<p><strong>In short.</strong> We do not ask for your name, email or phone number, and we never see your payment card. The game uses services from Google, Apple, Unity and Yandex to show ads, measure {"how the game is played" if g["analytics"] == "full" else "purchases and ad revenue"}, process purchases and keep your progress in the cloud. These services receive device identifiers and technical data. You can limit personalized ads at any time, and you can ask us to delete your data.</p>
</div>""")
    s.append(f"""<h2>1. Who we are</h2>
<p>This policy applies to the mobile game <strong>{name}</strong> (the “Game”) for Android and iOS, published by <strong>NoTriple-A Games</strong> (“we”, “us”). We are responsible for the data processed by the Game. Contact: {mail()}.</p>""")

    s.append("<h2>2. What data is processed</h2>")
    if g["playGames"]:
        acc = "If you are signed in to <strong>Google Play Games</strong> (Android) or <strong>Game Center</strong> (iOS), this player ID is linked to your Play Games or Game Center player ID so that your progress follows your account."
    else:
        acc = "On iOS, if you are signed in to <strong>Game Center</strong>, this player ID is linked to your Game Center player ID so that your progress follows your account."
    s.append(f"""<h3>2.1. Game progress and cloud save</h3>
<p>Your progress (levels, items, purchases made in the Game, settings) is stored on your device. To restore it after reinstalling or on a new device, the Game copies your save data to <strong>Unity Gaming Services</strong> (Authentication and Cloud Save). For this, Unity creates an anonymous player ID. {acc} We do not receive your Google or Apple email address or password.</p>""")

    if g["analytics"] == "full":
        an = "We use <strong>AppMetrica</strong> (by Yandex) to understand how the Game is played and to fix problems. AppMetrica collects: device model, operating system and its version, language, screen size, app version, device and installation identifiers (including the advertising ID where permitted), approximate location (country, city) derived from the IP address, and in-game events such as starting and finishing levels, in-game purchases, ad views and purchases."
    else:
        an = "We use <strong>AppMetrica</strong> (by Yandex) only to count purchases and ad revenue. AppMetrica collects: device model, operating system and its version, language, app version, device and installation identifiers (including the advertising ID where permitted), approximate location (country, city) derived from the IP address, purchase events and ad impressions with their revenue. Gameplay events are not sent."
    s.append(f"<h3>2.2. Analytics</h3>\n<p>{an}</p>")

    s.append(f"""<h3>2.3. Advertising</h3>
<p>The Game shows ads through <strong>Unity LevelPlay</strong> (formerly ironSource) mediation with these networks: {nets_html}. They may collect the advertising ID (AAID on Android, IDFA on iOS only with your permission), IP address, device information and ad interactions (impressions, clicks) to show ads, limit repetitive ads, prevent fraud and measure ad performance. Depending on your choices (section 4), ads may be personalized or non-personalized.</p>""")

    s.append("""<h3>2.4. Purchases</h3>
<p>In-app purchases are processed by <strong>Google Play</strong> or the <strong>App Store</strong>. We never receive your payment card or billing details. We receive the purchased product, its price and currency, the transaction ID and the store receipt, which we use to deliver the item, restore purchases and count revenue in analytics.</p>""")

    s.append("""<h3>2.5. Remote settings</h3>
<p>The Game downloads game settings (for example, how often ads are shown) from <strong>Unity Remote Config</strong>. This request includes the anonymous Unity player ID and basic device information.</p>""")

    other = []
    if g["notifications"]:
        other.append("Reminders are <strong>local notifications</strong> scheduled on your device; we do not use push tokens. The Game asks for permission first, and you can turn notifications off in your device settings.")
    if g["rating"]:
        other.append("The rating dialog is shown by Google Play or the App Store; your review goes directly to the store.")
    if g["share"]:
        other.append("If you share something from the Game, your device’s standard share menu is used; we do not see what you share or with whom.")
    n = 6
    if other:
        title = []
        if g["notifications"]: title.append("Notifications")
        if g["rating"]: title.append("ratings")
        if g["share"]: title.append("sharing")
        t = ", ".join(title[:-1]) + (" and " if len(title) > 1 else "") + title[-1]
        t = t[0].upper() + t[1:]
        s.append(f"<h3>2.{n}. {t}</h3>\n<p>{' '.join(other)}</p>")

    s.append("<p>We do not collect precise (GPS) location, contacts, photos, microphone or camera data.</p>")

    s.append("""<h2>3. Why we process data (legal bases)</h2>
<ul>
  <li><strong>To provide the Game</strong>, including cloud save and purchases — performance of our contract with you.</li>
  <li><strong>Analytics, fixing problems, fraud prevention, remote settings</strong> — our legitimate interest in keeping the Game working and improving it.</li>
  <li><strong>Personalized advertising</strong> — your consent, where the law requires it (EEA, UK, Switzerland). Non-personalized ads are shown on the basis of our legitimate interest in funding the free Game.</li>
</ul>""")

    choices = """<h2>4. Your choices</h2>
<ul>
  <li><strong>Consent (EEA, UK, Switzerland).</strong> On first launch the Game shows a consent form from Google. You can change your choice later in the Game’s settings (“Privacy settings”) where available, or by contacting us.</li>
  <li><strong>iOS tracking.</strong> The Game asks for permission under Apple’s App Tracking Transparency. Without permission, the IDFA is not accessed. You can change this in <em>Settings → Privacy &amp; Security → Tracking</em>.</li>
  <li><strong>Android advertising ID.</strong> You can reset or delete it in <em>Settings → Google → Ads</em> (or <em>Settings → Privacy → Ads</em>).</li>"""
    if g["notifications"]:
        choices += "\n  <li><strong>Notifications</strong> can be turned off in your device settings.</li>"
    choices += "\n</ul>"
    s.append(choices)

    links = ["  <li>Google AdMob, Google Play" + (", Google Play Games" if g["playGames"] else "") + ' — <a href="https://policies.google.com/privacy">policies.google.com/privacy</a></li>',
             '  <li>Unity Ads, Unity LevelPlay, Unity Gaming Services — <a href="https://unity.com/legal/game-player-and-app-user-privacy-policy">unity.com/legal/game-player-and-app-user-privacy-policy</a></li>',
             "  <li>" + ("Yandex Ads, AppMetrica" if g["yandexAds"] else "AppMetrica") + ' — <a href="https://yandex.com/legal/confidential/">yandex.com/legal/confidential</a></li>',
             '  <li>Apple App Store, Game Center — <a href="https://www.apple.com/legal/privacy/">apple.com/legal/privacy</a></li>']
    s.append("<h2>5. Third-party services</h2>\n<p>Each service processes data under its own privacy policy:</p>\n<ul>\n" + "\n".join(links) + """
</ul>
<p>We do not sell your personal data for money. Sharing device identifiers with ad networks for personalized advertising may be considered “sharing” or a “sale” under some US state laws; you can opt out as described in section 4.</p>""")

    s.append("""<h2>6. International transfers</h2>
<p>These providers may process data in the United States, the European Union, the Russian Federation and other countries. Where required, transfers are protected by safeguards such as the European Commission’s Standard Contractual Clauses used by the providers.</p>""")

    s.append("""<h2>7. How long data is kept</h2>
<ul>
  <li>Save data on your device — until you delete the Game.</li>
  <li>Cloud save — until you ask us to delete it (section 8), or until the Game’s cloud service is shut down.</li>
  <li>Analytics and advertising data — according to the retention periods of AppMetrica and the ad networks (see their policies).</li>
</ul>""")

    who = "your Google Play Games or Game Center nickname (if you use it)" if g["playGames"] else "your Game Center nickname (iOS, if you use it)"
    s.append(f"""<h2>8. Your rights</h2>
<p>Depending on where you live (for example, under the GDPR in the EEA and UK, the CCPA/CPRA and other US state laws, or Brazil’s LGPD), you may have the right to access your data, correct it, delete it, receive a copy, object to or restrict processing, withdraw consent at any time, and opt out of personalized advertising. We will not treat you differently for using these rights.</p>
<p>To use them, email us at {mail()}. Since we do not know your name, please include {who}, your device model and the approximate date you installed the Game, so we can find your data. We reply within 30 days. You also have the right to complain to your local data protection authority.</p>""")

    s.append(f"""<h2>9. Children</h2>
<p>The Game is not directed to children under 13 and we do not knowingly collect data from them. In the EEA, users under 16 should not consent to personalized ads without a parent. If you believe a child has provided data, contact us and we will delete it.</p>

<h2>10. Security</h2>
<p>Data is transferred over encrypted connections (HTTPS) and stored by the providers listed above using their security measures. No method of transfer or storage is 100% secure, but we take reasonable steps to protect your data.</p>

<h2>11. Changes to this policy</h2>
<p>We may update this policy when the Game changes. The new version is published on this page with a new effective date. If the changes are significant, we will also announce them in the Game or in its store listing.</p>

<h2>12. Contact</h2>
<p>NoTriple-A Games — {mail()}</p>""")
    return "\n\n".join(s)


def text_ru(g):
    name = html.escape(g["name"])
    nets = ["Google AdMob", "Unity Ads"] + (["Яндекс Реклама"] if g["yandexAds"] else [])
    nets_html = ", ".join(f"<strong>{n}</strong>" for n in nets[:-1]) + f" и <strong>{nets[-1]}</strong>"
    s = []
    s.append(f"""<div class="card">
<p><strong>Коротко.</strong> Мы не спрашиваем ваше имя, почту или телефон и никогда не видим данные банковской карты. Игра использует сервисы Google, Apple, Unity и Яндекса, чтобы показывать рекламу, {"понимать, как играют в игру" if g["analytics"] == "full" else "учитывать покупки и доход от рекламы"}, проводить покупки и хранить прогресс в облаке. Эти сервисы получают идентификаторы устройства и технические данные. Вы можете в любой момент ограничить персонализированную рекламу и попросить нас удалить ваши данные.</p>
</div>""")
    s.append(f"""<h2>1. Кто мы</h2>
<p>Политика действует для мобильной игры <strong>{name}</strong> («Игра») для Android и iOS, издатель — <strong>NoTriple-A Games</strong> («мы»). Мы отвечаем за данные, которые обрабатывает Игра. Связь: {mail()}.</p>""")

    s.append("<h2>2. Какие данные обрабатываются</h2>")
    if g["playGames"]:
        acc = "Если вы вошли в <strong>Google Play Игры</strong> (Android) или <strong>Game Center</strong> (iOS), этот ID связывается с вашим ID игрока Play Игр или Game Center, чтобы прогресс был привязан к аккаунту."
    else:
        acc = "На iOS, если вы вошли в <strong>Game Center</strong>, этот ID связывается с вашим ID игрока Game Center, чтобы прогресс был привязан к аккаунту."
    s.append(f"""<h3>2.1. Прогресс и облачное сохранение</h3>
<p>Прогресс (уровни, предметы, покупки в Игре, настройки) хранится на устройстве. Чтобы восстановить его после переустановки или на новом устройстве, Игра копирует сохранение в <strong>Unity Gaming Services</strong> (Authentication и Cloud Save). Для этого Unity создаёт анонимный ID игрока. {acc} Ваш адрес почты Google или Apple и пароль мы не получаем.</p>""")

    if g["analytics"] == "full":
        an = "Мы используем <strong>AppMetrica</strong> (Яндекс), чтобы понимать, как играют в Игру, и исправлять ошибки. AppMetrica собирает: модель устройства, операционную систему и её версию, язык, размер экрана, версию Игры, идентификаторы устройства и установки (в том числе рекламный ID, где это разрешено), примерное местоположение (страна, город) по IP-адресу, а также события в Игре: начало и прохождение уровней, внутриигровые покупки, просмотры рекламы и покупки."
    else:
        an = "Мы используем <strong>AppMetrica</strong> (Яндекс) только для учёта покупок и дохода от рекламы. AppMetrica собирает: модель устройства, операционную систему и её версию, язык, версию Игры, идентификаторы устройства и установки (в том числе рекламный ID, где это разрешено), примерное местоположение (страна, город) по IP-адресу, события покупок и показы рекламы с их доходом. Игровые события не отправляются."
    s.append(f"<h3>2.2. Аналитика</h3>\n<p>{an}</p>")

    s.append(f"""<h3>2.3. Реклама</h3>
<p>Реклама показывается через медиацию <strong>Unity LevelPlay</strong> (ранее ironSource) с сетями {nets_html}. Они могут собирать рекламный ID (AAID на Android, IDFA на iOS — только с вашего разрешения), IP-адрес, данные устройства и взаимодействие с рекламой (показы, нажатия), чтобы показывать рекламу, не повторять одно и то же, бороться с мошенничеством и измерять эффективность. В зависимости от вашего выбора (раздел 4) реклама может быть персонализированной или нет.</p>""")

    s.append("""<h3>2.4. Покупки</h3>
<p>Покупки в Игре проводят <strong>Google Play</strong> или <strong>App Store</strong>. Данные карты и платёжные реквизиты мы не получаем. Мы получаем купленный товар, цену и валюту, ID транзакции и чек магазина — чтобы выдать товар, восстановить покупки и учесть доход в аналитике.</p>""")

    s.append("""<h3>2.5. Удалённые настройки</h3>
<p>Игра загружает настройки (например, как часто показывать рекламу) из <strong>Unity Remote Config</strong>. В запрос входят анонимный ID игрока Unity и базовые данные устройства.</p>""")

    other = []
    if g["notifications"]:
        other.append("Напоминания — это <strong>локальные уведомления</strong>, которые планируются на самом устройстве; push-токены мы не используем. Игра сначала спрашивает разрешение, отключить уведомления можно в настройках устройства.")
    if g["rating"]:
        other.append("Окно оценки показывает Google Play или App Store, отзыв уходит напрямую в магазин.")
    if g["share"]:
        other.append("Если вы делитесь чем-то из Игры, используется стандартное меню «Поделиться» устройства; что и кому вы отправляете, мы не видим.")
    if other:
        title = []
        if g["notifications"]: title.append("уведомления")
        if g["rating"]: title.append("оценки")
        if g["share"]: title.append("«Поделиться»")
        t = ", ".join(title[:-1]) + (" и " if len(title) > 1 else "") + title[-1]
        t = t[0].upper() + t[1:]
        s.append(f"<h3>2.6. {t}</h3>\n<p>{' '.join(other)}</p>")

    s.append("<p>Мы не собираем точное местоположение (GPS), контакты, фото, данные микрофона и камеры.</p>")

    s.append("""<h2>3. Зачем мы обрабатываем данные (правовые основания)</h2>
<ul>
  <li><strong>Работа Игры</strong>, включая облачное сохранение и покупки, — исполнение договора с вами.</li>
  <li><strong>Аналитика, исправление ошибок, защита от мошенничества, удалённые настройки</strong> — наш законный интерес в том, чтобы Игра работала и становилась лучше.</li>
  <li><strong>Персонализированная реклама</strong> — ваше согласие там, где его требует закон (ЕЭЗ, Великобритания, Швейцария). Неперсонализированная реклама показывается на основании законного интереса — так Игра остаётся бесплатной.</li>
</ul>""")

    choices = """<h2>4. Ваш выбор</h2>
<ul>
  <li><strong>Согласие (ЕЭЗ, Великобритания, Швейцария).</strong> При первом запуске Игра показывает форму согласия Google. Изменить выбор можно позже в настройках Игры («Настройки конфиденциальности»), где они доступны, или написав нам.</li>
  <li><strong>Отслеживание на iOS.</strong> Игра спрашивает разрешение через App Tracking Transparency. Без разрешения IDFA не используется. Изменить: <em>Настройки → Конфиденциальность и безопасность → Отслеживание</em>.</li>
  <li><strong>Рекламный ID Android</strong> можно сбросить или удалить: <em>Настройки → Google → Реклама</em> (или <em>Настройки → Конфиденциальность → Реклама</em>).</li>"""
    if g["notifications"]:
        choices += "\n  <li><strong>Уведомления</strong> отключаются в настройках устройства.</li>"
    choices += "\n</ul>"
    s.append(choices)

    links = ["  <li>Google AdMob, Google Play" + (", Google Play Игры" if g["playGames"] else "") + ' — <a href="https://policies.google.com/privacy?hl=ru">policies.google.com/privacy</a></li>',
             '  <li>Unity Ads, Unity LevelPlay, Unity Gaming Services — <a href="https://unity.com/legal/game-player-and-app-user-privacy-policy">unity.com/legal/game-player-and-app-user-privacy-policy</a></li>',
             "  <li>" + ("Яндекс Реклама, AppMetrica" if g["yandexAds"] else "AppMetrica") + ' — <a href="https://yandex.ru/legal/confidential/">yandex.ru/legal/confidential</a></li>',
             '  <li>Apple App Store, Game Center — <a href="https://www.apple.com/ru/legal/privacy/">apple.com/legal/privacy</a></li>']
    s.append("<h2>5. Сторонние сервисы</h2>\n<p>Каждый сервис обрабатывает данные по своей политике:</p>\n<ul>\n" + "\n".join(links) + """
</ul>
<p>Мы не продаём персональные данные за деньги. Передача идентификаторов устройства рекламным сетям для персонализированной рекламы по законам некоторых штатов США может считаться «передачей» или «продажей»; отказаться от неё можно способами из раздела 4.</p>""")

    s.append("""<h2>6. Передача данных в другие страны</h2>
<p>Эти сервисы могут обрабатывать данные в США, Европейском союзе, Российской Федерации и других странах. Где это требуется, передача защищена мерами, которые применяют сами сервисы, например Стандартными договорными условиями Европейской комиссии.</p>""")

    s.append("""<h2>7. Сколько хранятся данные</h2>
<ul>
  <li>Сохранение на устройстве — пока вы не удалите Игру.</li>
  <li>Облачное сохранение — пока вы не попросите его удалить (раздел 8) или пока работает облачный сервис Игры.</li>
  <li>Данные аналитики и рекламы — по срокам AppMetrica и рекламных сетей (см. их политики).</li>
</ul>""")

    who = "ник в Google Play Играх или Game Center (если пользуетесь)" if g["playGames"] else "ник в Game Center (iOS, если пользуетесь)"
    s.append(f"""<h2>8. Ваши права</h2>
<p>В зависимости от места жительства (например, по GDPR в ЕЭЗ и Великобритании, CCPA/CPRA и законам других штатов США, LGPD в Бразилии, законодательству вашей страны о персональных данных) вы можете запросить доступ к данным, их исправление, удаление, копию, возразить против обработки или ограничить её, в любой момент отозвать согласие и отказаться от персонализированной рекламы. Использование этих прав никак не ухудшит для вас Игру.</p>
<p>Для этого напишите на {mail()}. Мы не знаем вашего имени, поэтому укажите {who}, модель устройства и примерную дату установки — так мы найдём ваши данные. Отвечаем в течение 30 дней. Вы также вправе подать жалобу в орган по защите персональных данных своей страны.</p>""")

    s.append(f"""<h2>9. Дети</h2>
<p>Игра не предназначена для детей младше 13 лет, и мы сознательно не собираем их данные. В ЕЭЗ пользователям младше 16 лет не следует давать согласие на персонализированную рекламу без родителей. Если вы считаете, что ребёнок передал нам данные, напишите нам — мы их удалим.</p>

<h2>10. Безопасность</h2>
<p>Данные передаются по зашифрованным соединениям (HTTPS) и хранятся у перечисленных сервисов с их мерами защиты. Ни один способ передачи и хранения не защищён на 100%, но мы принимаем разумные меры для защиты ваших данных.</p>

<h2>11. Изменения политики</h2>
<p>Мы можем обновлять политику при изменениях в Игре. Новая версия публикуется на этой странице с новой датой. О существенных изменениях мы также сообщим в Игре или на её странице в магазине.</p>

<h2>12. Контакты</h2>
<p>NoTriple-A Games — {mail()}</p>""")
    return "\n\n".join(s)


# ---------------------------------------------------------------- страницы
# ---------------------------------------------------------------- страницы

SITE = "https://notriplea.com"

ICON_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.6 1.8c-.3.3-.5.8-.5 1.4v17.6c0 .6.2 1.1.5 1.4l.1.1L13.5 12v-.2L3.7 1.7l-.1.1zm13.2 13.5L13.5 12v-.2l3.3-3.3.1.1 3.9 2.2c1.1.6 1.1 1.7 0 2.3l-3.9 2.2h-.1zm-.1.1L13.5 12 3.6 21.9c.4.4 1 .4 1.7.1l11.4-6.6M16.7 8.6 5.3 2c-.7-.4-1.3-.3-1.7.1l9.9 9.9 3.2-3.4z"/></svg>'
ICON_APPLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.4 12.6c0-2.5 2-3.6 2.1-3.7-1.2-1.7-3-1.9-3.6-2-1.5-.2-3 .9-3.8.9-.8 0-2-.9-3.3-.9-1.7 0-3.3 1-4.1 2.5-1.8 3.1-.5 7.6 1.3 10.1.8 1.2 1.8 2.6 3.1 2.5 1.3-.1 1.7-.8 3.3-.8 1.5 0 1.9.8 3.3.8 1.4 0 2.2-1.2 3-2.5 1-1.4 1.4-2.8 1.4-2.8s-2.7-1-2.7-4.1zM14 5.2c.7-.8 1.2-2 1-3.2-1 0-2.2.7-2.9 1.5-.6.7-1.2 1.9-1 3.1 1.1.1 2.2-.6 2.9-1.4z"/></svg>'

FAVICON = "data:image/svg+xml," + (
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E"
    "%3Cstop offset='0' stop-color='%23f97316'/%3E%3Cstop offset='1' stop-color='%23dc2626'/%3E"
    "%3C/linearGradient%3E%3C/defs%3E%3Crect width='64' height='64' rx='16' fill='url(%23g)'/%3E"
    "%3Ctext x='32' y='44' font-family='Arial,sans-serif' font-size='34' font-weight='900' "
    "text-anchor='middle' fill='white'%3EN%3C/text%3E%3C/svg%3E")


import hashlib
VER = hashlib.md5(open(os.path.join(ROOT, "style.css"), "rb").read() + open(os.path.join(ROOT, "assets/logo.png"), "rb").read()).hexdigest()[:8]
LOGO = "assets/logo.png"  # если файл есть — в шапке логотип вместо буквы N

UI = {
    "en": {
        "home": "/", "games": "Games", "contact": "Contact",
        "eyebrow": "Indie mobile games studio",
        "h1": "Brutal fights.<br><span>Epic heroes.</span>",
        "lead": "We’re a small indie team making games with a focus on atmosphere and combat. We want every hit to feel heavy and every fight to stay with you — whether it’s a Viking saga or a samurai duel. Beautiful, honest action that’s always in your pocket.",
        "btn_games": "Our games", "btn_contact": "Get in touch",
        "games_h": "Our games", "games_sub": "Free to play on Google Play and the App Store.",
        "privacy": "Privacy Policy", "soon": "soon",
        "contact_h": "Contact", "contact_sub": "Support, questions about your data, or just want to say hi — write to us.",
        "title": "NoTriple-A Games — mobile action games",
        "desc": "NoTriple-A Games is a small indie studio making action RPGs and tactical fighting games for Android and iOS.",
        "icon_alt": "icon",
    },
    "ru": {
        "home": "/ru/", "games": "Игры", "contact": "Контакты",
        "eyebrow": "Инди-студия мобильных игр",
        "h1": "Жёсткие бои.<br><span>Эпичные герои.</span>",
        "lead": "Мы — небольшая инди-команда и делаем игры с упором на атмосферу и боевую систему. Хотим, чтобы каждый удар ощущался, а каждый бой запоминался — будь то сага о викингах или самурайская дуэль. Красивый и честный экшен, который всегда под рукой.",
        "btn_games": "Наши игры", "btn_contact": "Написать нам",
        "games_h": "Наши игры", "games_sub": "Бесплатно в Google Play и App Store.",
        "privacy": "Политика конфиденциальности", "soon": "скоро",
        "contact_h": "Контакты", "contact_sub": "Поддержка, вопросы о данных или просто сказать привет — пишите.",
        "title": "NoTriple-A Games — мобильные экшен-игры",
        "desc": "NoTriple-A Games — небольшая инди-студия: экшен-RPG и тактические бои для Android и iOS.",
        "icon_alt": "иконка",
    },
}

# сохраняет выбор языка; на главной без выбора — русским отдаёт /ru/
LANG_JS = """<script>
(function(){
  try {
    document.querySelectorAll('[data-lang]').forEach(function(a){
      a.addEventListener('click', function(){ localStorage.setItem('lang', a.getAttribute('data-lang')); });
    });
    if (location.pathname === '/' && !localStorage.getItem('lang') &&
        /^ru|^uk|^be|^kk|^uz/i.test(navigator.language || '')) location.replace('/ru/');
  } catch (e) {}
})();
</script>"""


def brand():
    if os.path.exists(os.path.join(ROOT, LOGO)):
        return f'<img class="logo" src="/{LOGO}?v={VER}" alt="NoTriple-A Games" width="69" height="30">'
    return '<span class="mark">N</span>NoTriple-A Games'


def topbar(home, nav):
    return f"""<header class="topbar"><div class="inner">
  <a class="brand" href="{home}">{brand()}</a>
  <nav>{nav}</nav>
</div></header>"""


def lang_switch(lang, en_url, ru_url):
    en = '<strong>EN</strong>' if lang == "en" else f'<a href="{en_url}" data-lang="en">EN</a>'
    ru = '<strong>RU</strong>' if lang == "ru" else f'<a href="{ru_url}" data-lang="ru">RU</a>'
    return f'<span class="lang">{en} {ru}</span>'


def page(lang, title, desc, nav, body, url, alt_urls, image="/assets/icons/glory-ages-vikings.jpg"):
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{u}">' for l, u in alt_urls.items())
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0c0a09">
<link rel="canonical" href="{SITE}{url}">
{alts}
<link rel="icon" href="{FAVICON}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="NoTriple-A Games">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:image" content="{SITE}{image}">
<link rel="stylesheet" href="/style.css?v={VER}">
</head>
<body>
{topbar(UI[lang]["home"], nav)}

{body}

<footer class="site">
  <span>© NoTriple-A Games</span>
  <span><a href="mailto:{EMAIL}">{EMAIL}</a></span>
</footer>
{LANG_JS}
</body>
</html>
"""


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ", rel)


def store_buttons(g, t):
    b = []
    if g.get("googlePlay"):
        b.append(f'<a class="store" href="{g["googlePlay"]}" target="_blank" rel="noopener">{ICON_PLAY}Google Play</a>')
    else:
        b.append(f'<span class="store soon">{ICON_PLAY}Google Play — {t["soon"]}</span>')
    if g.get("appStore"):
        b.append(f'<a class="store" href="{g["appStore"]}" target="_blank" rel="noopener">{ICON_APPLE}App Store</a>')
    return "\n      ".join(b)


def tagline(g, lang):
    return g["tagline_ru"] if lang == "ru" else g["tagline"]


def build():
    eff = CFG["effective"]
    for g in CFG["games"]:
        name = html.escape(g["name"])
        icon = f"/assets/icons/{g['slug']}.jpg"
        en_url = f"/{g['slug']}/privacy/"
        ru_url = f"/{g['slug']}/privacy/ru/"
        alts = {"en": en_url, "ru": ru_url}
        for lang, rel, url, h1, eff_txt, text in (
                ("en", f"{g['slug']}/privacy/index.html", en_url, "Privacy Policy", f"Effective date: {eff['en']}", text_en(g)),
                ("ru", f"{g['slug']}/privacy/ru/index.html", ru_url, "Политика конфиденциальности", f"Дата вступления в силу: {eff['ru']}", text_ru(g))):
            chip = f'<div class="game-chip"><img src="{icon}" alt="" width="56" height="56"><div><strong>{name}</strong><br><span class="meta">{html.escape(tagline(g, lang))}</span></div></div>'
            desc = (f"Privacy Policy of the mobile game {name} by NoTriple-A Games." if lang == "en"
                    else f"Политика конфиденциальности мобильной игры {name} от NoTriple-A Games.")
            write(rel, page(lang, f"{h1} — {name}", desc, lang_switch(lang, en_url, ru_url),
                            f'<main class="doc">\n{chip}\n<h1>{h1}</h1>\n<p class="meta">{eff_txt}</p>\n\n{text}\n</main>',
                            url, alts, icon))

    for lang in ("en", "ru"):
        t = UI[lang]
        cards, mosaic = [], []
        for g in CFG["games"]:
            name = html.escape(g["name"])
            icon = f"/assets/icons/{g['slug']}.jpg"
            pol = f"/{g['slug']}/privacy/" + ("ru/" if lang == "ru" else "")
            cards.append(f"""  <li class="game">
    <div class="head">
      <img class="icon" src="{icon}" alt="{name} — {t['icon_alt']}" width="88" height="88" loading="lazy">
      <div><h3>{name}</h3><p class="tag">{html.escape(tagline(g, lang))}</p></div>
    </div>
    <div class="stores">
      {store_buttons(g, t)}
    </div>
    <div class="legal"><a href="{pol}">{t['privacy']}</a></div>
  </li>""")
        for _ in range(4):
            mosaic += [f'<img src="/assets/icons/{g["slug"]}.jpg" alt="">' for g in CFG["games"]]

        home = t["home"]
        body = f"""<section class="hero">
  <div class="mosaic" aria-hidden="true">{"".join(mosaic)}</div>
  <div class="content">
    <p class="eyebrow">{t['eyebrow']}</p>
    <h1>{t['h1']}</h1>
    <p class="lead">{t['lead']}</p>
    <a class="btn" href="#games">{t['btn_games']}</a>
    <a class="btn ghost" href="#contact">{t['btn_contact']}</a>
  </div>
</section>

<section class="section" id="games">
  <h2>{t['games_h']}</h2>
  <p class="sub">{t['games_sub']}</p>
  <ul class="games">
{chr(10).join(cards)}
  </ul>
</section>

<section class="contact" id="contact">
  <div class="section">
    <h2>{t['contact_h']}</h2>
    <p class="sub">{t['contact_sub']}</p>
    <div class="links">
      <a class="btn" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="btn ghost" href="https://t.me/NoTripleA" target="_blank" rel="noopener">Telegram</a>
      <a class="btn ghost" href="https://www.instagram.com/notriplea/" target="_blank" rel="noopener">Instagram</a>
    </div>
  </div>
</section>"""
        nav = f'<a href="{home}#games">{t["games"]}</a> <a href="{home}#contact">{t["contact"]}</a> ' + lang_switch(lang, "/", "/ru/")
        write("index.html" if lang == "en" else "ru/index.html",
              page(lang, t["title"], t["desc"], nav, body, home, {"en": "/", "ru": "/ru/", "x-default": "/"}))


if __name__ == "__main__":
    build()
