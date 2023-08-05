<h3 align="center">aadinspector</h3>

<p align="center"> This package will help to validate azure b2c jwt token.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

This package will help to validate azure b2c jwt token.

## 🏁 Getting Started <a name = "getting_started"></a>
- Dependancy & prerequisite 
    - Python >=3.6 should be installed.
    - "cryptography==37.0.4"
    - "PyJWT==2.4.0"
    - "requests==2.28.1"

- To Start experimenting this package you need to install it.

```
    pip install aadinspector
```
```
    # public key code should run only once on app start.
    pub_handler=  PublicKeyHandler("tenant_id")
    pub_handler.set_name_of_policy("name_of_policy")
    token="string"
    public_key= pub_handler.get_public_key(token)
    print(public_key)
    
    # token validation code should run for each request.
    jwt_validator = JWTValidator(public_key)
    is_valid, token = jwt_validator.validate(token)
    print(is_valid)
    print(token)

```

## ✍️ Authors <a name = "authors"></a>

- [Dinesh Kushwaha](https://pypi.org/user/dinesh-pypi/) - Idea & Initial work

See also the list of [contributors](https://github.com/dinesh-kushwaha) who participated in this project.