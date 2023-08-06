# DSM Email

## install
```
pip install dsmemail
```

## how to use
1. set env

```
DSM_EMAIL_URI=<DSM_EMAIL_URI>
DSM_EMAIL_APIKEY=<DSM_EMAIL_APIKEY>
```

2. send email

```python
import dsmemail

status, msg = dsmemail.sendEmail(
    subject="test", 
    message="helloworld", 
    emails=["admin@admin.com"]
)

print(status, msg)
```
output
```
(True, 'email send sucess')
```

#
status
```
True = send email sucess
False = send email fail
```

msg
```
string describe status
```