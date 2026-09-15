# Django Real-Time Chat Application

A real-time, multi-room chat application built with **Django** and **Django Channels**, featuring user authentication, persistent message history, join/leave notifications, and emoji shortcode rendering.

This project satisfies the Advanced tier of the Chat Application task: a full web-based GUI (instead of a desktop tkinter window), user registration/login backed by SQLite, multiple named chat rooms, message history on join, focus-based notifications, and emoji shortcode support.

---

## Tech Stack

- **Python 3** / **Django** — core web framework, ORM, authentication
- **Django Channels** — adds ASGI + WebSocket support to Django for real-time, bidirectional messaging
- **Daphne** — ASGI server used by `runserver` in development
- **SQLite** — default Django database; stores users, rooms, and message history
- **In-memory channel layer** (`channels.layers.InMemoryChannelLayer`) — routes messages between WebSocket connections on a single process (no Redis dependency)
- **Vanilla JavaScript** (WebSocket API, Notification API) — frontend real-time logic, no additional JS framework

---

## How It Works (Architecture)

1. **`asgi.py`** is the entry point for every incoming connection. It inspects whether the connection is a normal HTTP request or a WebSocket upgrade:
   - HTTP requests → handled by standard Django views (login, registration, room list, room page).
   - WebSocket connections → passed through `AuthMiddlewareStack` (so the connected user is known) and then to `chat/routing.py`.
2. **`chat/routing.py`** matches the WebSocket URL (`ws/chat/<room_name>/`) to `ChatConsumer`.
3. **`chat/consumers.py`** (`ChatConsumer`) is the core real-time logic:
   - `connect()` — joins a "channel group" named after the room, sends a join notice to everyone else in the room, and sends the requesting user their room's message history.
   - `receive()` — saves each incoming message to the database, then broadcasts it to everyone in the room's group.
   - `disconnect()` — removes the user from the group and broadcasts a "has left the chat" notice.
   - `chat_message()` / `system_message()` — handlers that push broadcasted events back down each connected client's own socket.
4. **`chat/models.py`** defines `Room` (name, creator) and `Message` (room, sender, content, timestamp) — this is what makes message history persistent across sessions, not just live in-memory.
5. **Frontend (`room.html`)** opens a WebSocket connection via JavaScript, sends typed messages as JSON, and renders incoming messages (including system notices and emoji-rendered text) into the page live, without reloading.

Because everyone talks *through the server* (not directly to each other), the server can persist messages, enforce authentication, and broadcast to many clients in a room at once — this is the key difference from the Beginner-tier two-socket CLI version.

---

## Setup & Installation

```bash
# 1. Clone/enter the project directory
cd chatproject

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install django channels daphne

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Run the development server
python manage.py runserver
```

The app will be available at `http://localhost:8000/`.

> **Note:** This project uses Django Channels' `InMemoryChannelLayer`, so it runs entirely on a single process with no external services (like Redis) required. This is suitable for local development and demonstration, but not for a multi-process production deployment — see **Limitations** below.

---

## Usage

1. Visit `http://localhost:8000/register/` to create an account (username + password).
2. You'll be logged in automatically and redirected to the room list (`/chat/`).
3. Type a room name and click **Join / Create** — if the room doesn't exist yet, it's created; if it does, you join it.
4. Start chatting. Messages show as `[HH:MM] username: message`.
5. Open the same room URL in a second browser (or an incognito window, logged in as a different user) to test real-time messaging between two people.
6. Click **Enable Notifications** once to allow desktop notifications for new messages that arrive while the tab isn't focused.
7. Type emoji shortcodes like `:smile:`, `:heart:`, `:thumbsup:`, `:fire:`, `:wave:`, `:tada:` — these render as Unicode emoji automatically.

---

## Feature Checklist

- [x] Server component listening for connections (Django Channels `ChatConsumer` over ASGI/WebSocket)
- [x] Client (browser-based, via WebSocket JavaScript)
- [x] Real-time, bidirectional messaging
- [x] Timestamp-prefixed messages (`[14:35] Alice: Hello`)
- [x] Graceful disconnect handling — other users are notified when someone leaves
- [x] Runs entirely on localhost for local testing
- [x] Web-based GUI (Django templates + JavaScript, in place of tkinter)
- [x] User registration & login (SQLite-backed, via Django's built-in auth system)
- [x] Multiple named chat rooms — create or join by name
- [x] Message history loaded on joining a room
- [x] Desktop notification for new messages when the window isn't focused
- [x] Emoji shortcode rendering (`:smile:` → 😄)

---

## Known Limitations

- **Channel layer:** Uses `InMemoryChannelLayer`, which only works correctly with a single server process. A production or multi-worker deployment would need `channels_redis` as the channel layer backend so broadcasts reach clients connected to *different* processes.
- **Notifications:** Rely on the browser's `Notification` API and the OS's own notification permissions (e.g. macOS System Settings → Notifications, and Focus/Do Not Disturb mode can silently suppress them). Notifications currently fire for all incoming messages while the tab is hidden, including the sender's own messages echoed back to them.
- **Emoji shortcodes:** Handled via a small hardcoded JavaScript lookup table (`emojiMap` in `room.html`) covering common shortcodes — not the full emoji shortcode standard.
- **No production deployment configuration:** `DEBUG = True` and the Django development server (via Daphne) are used throughout; see [Django's deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/) before deploying this anywhere public.

---

## Project Structure

```
chatproject/
├── chatproject/
│   ├── settings.py       # ASGI_APPLICATION, CHANNEL_LAYERS, INSTALLED_APPS
│   ├── asgi.py           # ProtocolTypeRouter: HTTP vs WebSocket routing
│   └── urls.py           # Top-level URL routes (chat, login, logout, register)
├── chat/
│   ├── models.py         # Room, Message models
│   ├── views.py          # register, chat_home, room views
│   ├── urls.py           # HTTP routes for the chat app
│   ├── routing.py        # WebSocket URL routing → ChatConsumer
│   ├── consumers.py      # Core real-time chat logic (connect/receive/disconnect)
│   └── templates/chat/
│       ├── home.html     # Room list / create-or-join form
│       ├── room.html     # The live chat window (WebSocket JS lives here)
│       ├── login.html
│       └── register.html
└── manage.py
```