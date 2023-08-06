from cryptography.fernet import Fernet

def protect(key):
    try:
        return Fernet(key=key)
    except Exception as en:
        print(str(en))

def genKey():
    try:
        return Fernet.generate_key()
    except Exception as en:
        print(str(en))

def enc_file_name(file):
    try:
        return Fernet.encrypt(file)
    except Exception as en:
        print(str(en))

def decrypt_file(file):
    try:
        return Fernet.decrypt(file)
    except Exception as en:
        print(str(en))

def del_file(file):
    try:
        import os
        os.system(f'del {file}')
    except Exception as en:
        print(str(en))

def add_file(name, message: None):
    try:
        if message == None:
            try:
                print()
            except Exception as en:
                print(str(en))
        else:
            with open(f'{name}', 'w') as f:
                f.write(message)
                f.close()
    except Exception as en:
        print(str(
            en
        ))
