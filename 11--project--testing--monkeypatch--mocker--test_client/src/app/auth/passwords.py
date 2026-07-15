from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    # from app.services.users import repository
    #
    # user = repository.get_by_username("admin")
    # print("user", user)
    # print("password_hash:", repr(user.password_hash) if user else None)
    # if user:
    #     print("verify:", password_hash.verify("admin", user.password_hash))

    return password_hash.verify(plain, hashed)
