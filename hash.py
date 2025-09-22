from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# A senha que você quer usar no login
senha_correta = "senhaForte123"
hash_correto = pwd_context.hash(senha_correta)

print(f"O hash correto para '{senha_correta}' é:")
print(hash_correto)