# FakeEmail
### to install:
```bash
pip install FakeEmail  
```
### Example
```python
from FakeEmail import Email


mail=Email().Mail()
print(mail)



while True:
	mass=Email(mail["session"]).inbox()
	if mass:
		print(mass)
		break
	
```

### Follow us on social media accounts

* telegram : @DIBIBl ; @TDTDI
* instgram : @_v_go
* github : https://github.com/muntazir-halim