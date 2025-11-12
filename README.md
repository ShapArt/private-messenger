# 🛡️📡 Private Messenger (E2EE) — Design + MVP stubs

[![CI](https://github.com/ShapArt/private-messenger/actions/workflows/ci.yml/badge.svg)](https://github.com/ShapArt/private-messenger/actions/workflows/ci.yml) [![license](https://img.shields.io/github/license/ShapArt/private-messenger)](https://github.com/ShapArt/private-messenger/blob/main/LICENSE)






<table>


<tr>


<td><b>✨ Что умеет</b><br/>Короткий список возможностей, ориентированных на ценность.</td>


<td><b>🧠 Технологии</b><br/>Стек, ключевые решения, нюансы безопасности.</td>


<td><b>🖼️ Демо</b><br/>Скриншот/гиф или ссылка на Pages.</td>


</tr>


</table>





> [!TIP]


> Репозиторий оформлен по правилам: Conventional Commits, SemVer, CHANGELOG, SECURITY policy и CI.


> Секреты — только через `.env`/секреты репозитория.








<p align="left">


  <img alt="build" src="https://img.shields.io/github/actions/workflow/status/ShapArt/private-messenger/ci.yml?label=CI&logo=githubactions">


  <img alt="license" src="https://img.shields.io/github/license/ShapArt/private-messenger">


  <img alt="last commit" src="https://img.shields.io/github/last-commit/ShapArt/private-messenger">


  <img alt="issues" src="https://img.shields.io/github/issues/ShapArt/private-messenger">


  <img alt="stars" src="https://img.shields.io/github/stars/ShapArt/private-messenger?style=social">


</p>








Цель: приватный мессенджер с end‑to‑end шифрованием, самохостингом и Web/CLI‑клиентом.


- Сигналоподобный протокол (Double Ratchet), сторедж на сервере — **только** шифротексты.


- Транспорт: HTTPS/WebSocket. Верификация устройств по safety‑number.


- Минимум метаданных: таймстемпы с шумом, удаление по TTL.





## Папки


- `design/` — протокол, потоки, угрозмодель


- `server/` — FastAPI + websockets (скелет), выдача pre‑keys, приём зашифрованных сообщений


- `client-web/` — scaffold (Vite) с WebCrypto API (заглушки)





> Внимание: это учебно‑демо проект, не для продакшн‑секьюрной связи без аудита.





## Быстрый старт





*Заполнить по мере развития проекта.*








## Архитектура





*Заполнить по мере развития проекта.*








## Конфигурация





*Заполнить по мере развития проекта.*








## Тесты





*Заполнить по мере развития проекта.*








## Roadmap





*Заполнить по мере развития проекта.*


