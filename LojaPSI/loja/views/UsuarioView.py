from django.shortcuts import get_object_or_404, render
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm


def list_usuario_view(request, id=None):
    usuarios = Usuario.objects.filter(perfil=2)
    return render(request, 'usuario/usuario.html', {'usuarios': usuarios})


def edit_usuario_view(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    message = None

    if request.method == 'POST':
        usuarioForm = UserUsuarioForm(request.POST, instance=usuario)
        userForm = UserForm(request.POST, instance=request.user)
        email = request.POST.get('email', '').strip()
        emailUnused = not Usuario.objects.filter(user__email__iexact=email).exclude(user__id=request.user.id).exists()

        if usuarioForm.is_valid() and userForm.is_valid() and emailUnused:
            usuarioForm.save()
            userForm.save()
            message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
        elif not emailUnused:
            message = {'type': 'warning', 'text': 'E-mail já usado'}
        else:
            message = {'type': 'danger', 'text': 'Dados inválidos'}
    else:
        usuarioForm = UserUsuarioForm(instance=usuario)
        userForm = UserForm(instance=request.user)

    return render(request, 'usuario/usuario-edit.html', {
        'usuarioForm': usuarioForm,
        'userForm': userForm,
        'message': message,
    })
