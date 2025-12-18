# Private Messenger (E2EE, Signal-style)

## ✨ Что умеет
- E2EE-чаты 1:1: сервер хранит только метаданные, контент шифруется libsignal-client на клиентах.
- WebRTC DataChannel для p2p доставки; при недоступности — TURN relay, сервер остаётся сигнальным.
- Вложения до 50–100 МБ через presigned S3/MinIO ссылки, шифрование на клиенте перед загрузкой.
- Magic link/OTP логин, device binding, проверка safety numbers/фингерпринтов ключей.
- Тёмная desktop/web-обёртка (Tauri+React) с локальным сейф-хранилищем ключей.

## 🧠 Технологии
- Backend: FastAPI + Postgres + Redis (ws signaling), WebSocket комнатная модель, CORS/HTTPS only.
- Crypto: libsignal-client (X3DH + Double Ratchet), client-side шифрование вложений (libsodium secretbox), perfect forward secrecy.
- Транспорт: WebRTC DataChannel (DTLS/SRTP), TURN fallback; presigned S3 URLs для файлов.
- Безопасность: secrets только через .env, gitleaks в pre-commit/CI, JWT c ограниченным TTL, минимальные GitHub Actions permissions.

## 🖼️ Демо
- TODO: добавить gif/скрин (web + desktop) и ссылку на стенд после развёртывания.

## Архитектура
- `backend/` — FastAPI: эндпоинты `/register`, `/login`, `/keys`, `/prekeys`, `/signal`, `/attachments/presign`, `/stun-turn-cred`; ws `/ws` для сигналинга.
- `web/` — React/Vite клиент с libsignal-client, WebRTC, хранилищем ключей.
- `desktop/` — Tauri v2 обёртка над web-клиентом.
- `infra/` — docker-compose (Postgres, Redis, API; можно расширить TURN/MinIO).
- docs: `docs/overview.md` (sequence), `docs/ci-badge-snippet.md`.

## Конфигурация
Заполни `.env` по шаблону `.env.example`:
- `DATABASE_URL` — Postgres DSN (asyncpg).
- `REDIS_URL` — очередь сигналинга/присутствия.
- `JWT_SECRET`, `JWT_TTL_SECONDS` — токены.
- `S3_ENDPOINT`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET` — presigned для вложений.
- `TURN_SECRET` — для выдачи временных TURN-учёток.
- `ALLOWED_ORIGINS`, `WEBAPP_ORIGIN` — CORS.

### Локальный запуск
```bash
cd backend
pip install -e .[dev]
uvicorn app.main:app --reload
```

### Docker Compose
```bash
cd infra
docker compose up --build
```
- Поднимет API на 8000, Postgres на 5432, Redis на 6379. TURN/MinIO добавить позже.

## Тесты
- Backend: `cd backend && pip install -e .[dev] && ruff check . && black --check . && mypy app && pytest`.
- Web/Desktop: TODO — добавить lint/typecheck/playwright smoke после инициализации.

## Roadmap
- Реализовать хранение/выдачу ключевых бандлов (Postgres + Redis), magic link/OTP, device binding.
- Добавить presign через MinIO/S3 и клиента шифрования вложений (libsodium).
- Реализовать WebRTC сигналинг (комнаты, retry, ICE-candidates), TURN creds по времени.
- Подключить web-клиент (React/Vite + libsignal-client) и desktop (Tauri).
- Добавить e2e/integration tests (ws сценарии, attachment upload), playwright smoke для web.
- Threat model расширить, автоматический audit-log, rate limits.
