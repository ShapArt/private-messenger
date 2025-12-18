# Private Messenger — overview

## Sequence: device registration + message
```mermaid
sequenceDiagram
  participant ClientA
  participant API
  participant Postgres
  participant Redis
  participant ClientB

  ClientA->>API: POST /register (identity key, signed/one-time prekeys)
  API->>Postgres: store device + prekeys
  ClientA->>API: POST /signal (session init payload)
  API->>Redis: enqueue signal for ClientB
  Redis-->>ClientB: ws push (ciphertext)
  ClientA-->>ClientB: WebRTC DTLS/SRTP (DataChannel, encrypted)
  ClientA->>API: POST /attachments/presign (metadata)
  API-->>ClientA: presigned PUT/GET URL
  ClientA-->>S3: upload encrypted blob
  ClientB-->>S3: download encrypted blob
```

## Components
- FastAPI (signaling, auth, presign).
- Redis pub/sub for WebSocket fanout.
- Postgres for users/devices/prekeys.
- TURN for relay fallback; WebRTC DataChannels for payloads.
