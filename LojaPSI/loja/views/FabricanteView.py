from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from loja.models import Fabricante, Produto


def fabricante_listar(request):
    fabricantes = Fabricante.objects.all()
    return render(request, 'fabricante/fabricante.html', {'fabricantes': fabricantes})


@login_required
def fabricante_criar(request):
    if request.method == 'POST':
        nome = request.POST.get('fabricante', '').strip()
        if not nome:
            messages.error(request, 'Informe o nome do fabricante.')
        elif Fabricante.objects.filter(fabricante__iexact=nome).exists():
            messages.warning(request, 'Esse fabricante já existe.')
        else:
            Fabricante.objects.create(fabricante=nome)
            messages.success(request, 'Fabricante criado com sucesso.')
            return redirect('fabricantes')
    return render(request, 'fabricante/fabricante-create.html')


@login_required
def fabricante_editar(request, id):
    fabricante = get_object_or_404(Fabricante, id=id)
    if request.method == 'POST':
        nome = request.POST.get('fabricante', '').strip()
        if not nome:
            messages.error(request, 'Informe o nome do fabricante.')
        elif Fabricante.objects.filter(fabricante__iexact=nome).exclude(id=id).exists():
            messages.warning(request, 'Esse fabricante já existe.')
        else:
            fabricante.fabricante = nome
            fabricante.save()
            messages.success(request, 'Fabricante atualizado com sucesso.')
            return redirect('fabricantes')
    return render(request, 'fabricante/fabricante-edit.html', {'fabricante': fabricante})


@login_required
def fabricante_excluir(request, id):
    fabricante = get_object_or_404(Fabricante, id=id)
    if request.method == 'POST':
        nome = fabricante.fabricante
        fabricante.delete()
        messages.success(request, f'Fabricante "{nome}" excluído com sucesso.')
        return redirect('fabricantes')
    return render(request, 'fabricante/fabricante-delete.html', {'fabricante': fabricante, 'quantidade_produtos': Produto.objects.filter(fabricante=fabricante).count()})
