# Решение
line-provider:

При создании события(подразумеватся что оно новое) кладется в redis с временем жизни ключа(deadline). 

При обновлении события в redis с помощью pub/sub отправляется изменения.

Также все действия записываются в базу для истории.

bet-maker:

Получает все события из redis(т.к лежат только новые живые по времени события)

Создает ставку по uuid из события и наличия его в redis.

Возвращает все записи.

Изменения статуса происходят благодоря redis(pub/sub)

# Запуск приложения

make create_network

make generate_configs

sudo make bu 

make migrate service=bet-maker

make migrate service=line-provider

У всего есть swagger можно создавать там события и ставки.
При создании события важно чтобы deadline был позднее текущего времени, иначе будет ошибка

Пример: "deadline": "2022-07-11T12:25:26.239Z" - текущее, то "deadline": "2022-07-11T14:25:26.239Z" - позднее на 2 часа

В обновлении события в теле запроса можно оставлять так:
{
  "state": "finished_win"
}