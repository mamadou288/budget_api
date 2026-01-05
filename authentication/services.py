from django.contrib.auth import get_user_model

User = get_user_model()


def is_email_taken(email: str) -> bool:
    return User.objects.filter(email__iexact=(email or "")).exists()


def authenticate_by_email(email: str, password: str):
    """
    Retourne un user si credentials valides, sinon None.
    """
    if not email or not password:
        return None

    user = User.objects.filter(email__iexact=email).first()
    if user is None:
        return None

    if not user.is_active:
        return None

    if not user.check_password(password):
        return None

    return user


def create_user_with_email(email: str, password: str):
    """
    Crée un user (hash password) et renvoie l'objet.
    Lève ValueError si email déjà pris.
    """
    if is_email_taken(email):
        raise ValueError("EMAIL_TAKEN")

    return User.objects.create_user(
        username=email,  # champ interne Django
        email=email,
        password=password,
    )


def is_username_taken(username: str) -> bool:
    return User.objects.filter(username__iexact=(username or "")).exists()


def create_user_account(
    *,
    email: str,
    username: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
):
    if is_email_taken(email):
        raise ValueError("EMAIL_TAKEN")
    if is_username_taken(username):
        raise ValueError("USERNAME_TAKEN")

    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

