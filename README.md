# PyCord

A **Discord-inspired realtime messenger built fullstack in Django**

## Stack

| Layer    | Tooling                                                        |
| -------- | -------------------------------------------------------------- |
| Web      | Django 5.1 + Daphne (ASGI)                                     |
| Realtime | django-channels + channels-redis                               |
| Auth     | django-allauth (email + GitHub OAuth + passkeys )              |
| Headless | allauth.headless mounted at `/_allauth/`                     |
| API      | Django REST Framework (CursorPagination, Token + Session auth) |
| Admin    | django-admin-interface + search-admin-autocomplete             |
| DB       | Postgres (Supabase-friendly via `?sslmode=require`)          |
| Config   | django-environ + django-service-urls                           |
| IDs      | django-puid (short, URL-safe public IDs)                       |
| Styling  | django-tailwind-cli + DaisyUI + django-allauth-ui              |
| Deploy   | Fly.io + Docker + Whitenoise                                   |

## License

MIT.
