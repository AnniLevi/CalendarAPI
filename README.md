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
    "country": 10
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


### Get token

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


**Note:**
*For all of the following requests insert the token into the request header, for example:*
*headers = {"Authorization": "Token 0f9ccdafdd2d356d5215ae08ecf12ac9903bd307"}*


### Create event

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
    "name": "event1",
    "datetime_start": "2021-07-15T15:30:00+03:00",
    "time_end": "16:00:00",
    "remind_unit": 60,
    "number_of_remind_units": 5
}
```