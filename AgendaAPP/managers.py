from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, nombreUsuario, password, **extrafields):
        if not nombreUsuario:
            raise ValueError('Ingrese un nombre d eusuario')
        # nombreUsuario = self.normalize_user(nombreUsuario)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nombreUsuario, password, **extrafields):
        extrafields.setdefault('is_superuser', False)
        return self._create_user(nombreUsuario, password, **extrafields)

    def create_superuser(self, nombreUsuario, password, **extrafields):
        extrafields.setdefault('is_superuser', True)

        if extrafields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(nombreUsuario, password, **extrafields)
