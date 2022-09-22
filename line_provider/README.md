# Line provider (test bet provider)

## Urls:
- `GET /event/{event_id}/` (Получение информации о событии)
- `GET /event/closed/` (Информация о завершившихся событиях. Статусы: WIN, LOSE)
- `POST /event/ -d "coefficient: Decimal, deadline: datetime"` (Создание события)
- `PATCH /event/{event_id}/ -d "state: EventState | None, coefficient: Decimal | None, win_amount: float | None"` (Обновление информации о событии. Данные передаются в `bet_maker`)
- `GET /event/active/` (Информация о доступных для ставки событиях)
- `GET /event/history/` (Информация о всех событиях)
- `POST /event/bet/{event_id}/ -d "bet_amount"` (Коллбек для постановки ставки сервисом `bet_maker`)

### Стек:
- FastAPI
- Httpx
- loguru
- Docker
