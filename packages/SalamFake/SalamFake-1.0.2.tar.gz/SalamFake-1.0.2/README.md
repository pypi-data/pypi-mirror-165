# SalamFake
### to install:
```bash
pip install SalamFake  
```
### Example
```python
from SalamFake import Email


mail=Email().Mail()
print(mail)



while True:
	mass=Email(mail["session"]).inbox()
	if mass:
		print(mass)
		break
	
```

### Follow us on social media accounts

* telegram : @T5B55
