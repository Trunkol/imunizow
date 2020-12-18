
from django.contrib.auth.models import Group, User
from gestao.models import PessoaFisica

def save_pessoa_fisica(backend, user, response, *args, **kwargs):
	if backend.name == 'sabia':
		cpf = response.get('cpf')
		
		kwargs['request'].session['foto_usuario'] = response.get('avatar', None)

		if not PessoaFisica.objects.filter(cpf=cpf).exists():
			pessoa_fisica = PessoaFisica()
			pessoa_fisica.nome = response.get('name')
			pessoa_fisica.cpf = cpf
			pessoa_fisica.email = response.get('email')
			pessoa_fisica.user = user
			pessoa_fisica.save()
			if not user.is_staff:
				user.is_staff = True
				user.save()
			return {'user': user, 'is_new': True}
		return {'user': user, 'is_new': False}

def associate_by_username(backend, details, user=None, *args, **kwargs):
	"""
	Associate current auth with a user with the same username in the DB.

	This pipeline entry is not 100% secure unless you know that the providers
	enabled enforce email verification on their side, otherwise a user can
	attempt to take over another user account by using the same (not validated)
	email address on some provider.  This pipeline entry is disabled by
	default.
	"""
	if user:
		return None

	username = details.get('username')
	if username:
		# Try to associate accounts registered with the same username,
		# only if it's a single object. AuthException is raised if multiple
		# objects are returned.
		users = list(User.objects.filter(username__iexact=username))
		if len(users) == 0:
			return None
		elif len(users) > 1:
			raise AuthException(
				backend,
				'The given username is associated with another account'
			)
		else:
			return {'user': users[0],
					'is_new': False}
