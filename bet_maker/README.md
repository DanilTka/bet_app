# Bet maker

## Urls:
- `GET /events/` (получение информации о доступных событиях для ставок)
- `POST /bet/{event_id}/ -d "bet_amount"` (создание ставки на доступное событие)
- `POST /callback/bet/{event_id}/` (коллбек для получения обновленных данных по сделанным ставкам)
- `GET /bets/` (история ставок)

### Стек:
- FastAPI
- SQLAlchemy, alembic
- PostgreSQL
- loguru
- Docker
