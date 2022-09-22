# Bet maker

## Urls:
- `GET /events/` (Получение информации о доступных событиях для ставок)
- `POST /bet/{event_id}/ -d "bet_amount"` (Создание ставки на доступное событие)
- `POST /callback/bet/{event_id}/` (Коллбек для получения обновленных данных по сделанным ставкам)
- `GET /bets/` (История ставок)

### Стек:
- FastAPI
- SQLAlchemy, alembic
- PostgreSQL
- Httpx
- loguru
- Docker
