from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from loja.models import Categoria, Produto


def categoria_listar(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/categoria.html', {'categorias': categorias})


@login_required
def categoria_criar(request):
    if request.method == 'POST':
        nome = request.POST.get('Categoria', '').strip()
        if not nome:
            messages.error(request, 'Informe o nome da categoria.')
        elif Categoria.objects.filter(Categoria__iexact=nome).exists():
            messages.warning(request, 'Essa categoria já existe.')
        else:
            Categoria.objects.create(Categoria=nome)
            messages.success(request, 'Categoria criada com sucesso.')
            return redirect('categorias')
    return render(request, 'categoria/categoria-create.html')


@login_required
def categoria_editar(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        nome = request.POST.get('Categoria', '').strip()
        if not nome:
            messages.error(request, 'Informe o nome da categoria.')
        elif Categoria.objects.filter(Categoria__iexact=nome).exclude(id=id).exists():
            messages.warning(request, 'Essa categoria já existe.')
        else:
            categoria.Categoria = nome
            categoria.save()
            messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect('categorias')
    return render(request, 'categoria/categoria-edit.html', {'categoria': categoria})


@login_required
def categoria_excluir(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        nome = categoria.Categoria
        categoria.delete()
        messages.success(request, f'Categoria "{nome}" excluída com sucesso.')
        return redirect('categorias')
    return render(request, 'categoria/categoria-delete.html', {'categoria': categoria, 'quantidade_produtos': Produto.objects.filter(categoria=categoria).count()})
