# CalendarAPI

Back-end (REST API) for application with authorization, the ability to add custom events and notifications about upcoming events and holidays in user's country by e-mail.
Periodic update of the list of holidays.

____

### Registration

To register, follow the link:
> /register/

Request (POST-method):
```
{
    "email": "email@email.email",
    "password": "testpassword",
    "country": 19
}
```
Enter country id

Response:
```
{
    "user": 
    {
        "id": 1,
        "email": "email@email.email",
        "country": 10
    },
    "token": "a32fa4cab52abb53c71ca35dcb312beb7742519d"
}
```
You will receive a message with a token by email


### Getting token

If the token is lost, you can restore it (or get a new one)
> /get_token/

Request (POST-method):
```
{
    "email": "email@email.email",
    "password": "testpassword"
}
```

Response:
```
{
"token": "a32fa4cab52abb53c71ca35dcb312beb7742519d"
}
```
You will receive a message with a token by email


**Note:**
*For all of the following requests insert the token into the request header, for example:*
*headers = {"Authorization": "Token 0f9ccdafdd2d356d5215ae08ecf12ac9903bd307"}*


### Create an event

> /create_event/

Request (POST-method):
```
{
    "name": "test_event",
    "datetime_start": "2021-07-15T15:30:00+03:00",
    "time_end": "16:00:00",
    "remind_unit": 60,
    "number_of_remind_units": 5
}
```

- "datetime_start" - enter date and start time of event (required field)  
- "time_end" - enter time end of event (default = "23:59:59")  
- If you would like to receive a reminder of an event on your email, set a value for the time units for the reminder -  "remind_unit" field.
Possible values:  
> 60 - minutes,  
> 3600 - hours,  
> 86400 - days,  
> 604800 - weeks.  

- "number_of_remind_units" - default = 1.

Response:
```
{
    "id": 1,
    "name": "test_event",
    "datetime_start": "2021-07-15T15:30:00+03:00",
    "time_end": "16:00:00",
    "remind_unit": 60,
    "number_of_remind_units": 5
}
```

### Getting a list of events for the day

> /events_for_day/?date=2021-08-15

Request (GET-method with params)

Response:
```
[
    {
        "id": 1,
        "name": "test_event",
        "datetime_start": "2021-07-15T15:30:00+03:00",
        "time_end": "16:00:00",
        "remind_unit": 60,
        "number_of_remind_units": 5
    },
    {
        ...
    }
]
```

### Getting the general aggregation of events by day for the month

> /events_for_month/?month=7

Request (GET-method with params)


Response:
```
{
    "2021-08-15": [
        {
            "id": 1,
            "name": "test_event",
            "datetime_start": "2021-08-15T15:30:00+03:00",
            "time_end": "16:00:00",
            "remind_unit": 60,
            "number_of_remind_units": 5
        },
        {
            ...
        }
    ],
    "2021-08-16": [
        {
            ...
        }
    ],
    ...
}
```

### Getting a list of holidays for the month

> /holidays_for_month/?month=5

Request (GET-method with params)

Response:
```
[
    {
        "id": 778,
        "name": "Labour Day",
        "date_start": "2021-05-01",
        "date_end": "2021-05-02"
    },
    {
        "id": 779,
        "name": "Victory Day",
        "date_start": "2021-05-09",
        "date_end": "2021-05-10"
    },
   {
            ...
    },
]
```

You will receive a list of all holidays for the month in the user's country
