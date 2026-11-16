from decimal import Decimal, InvalidOperation
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from loja.models import Categoria, Fabricante, Produto


def _boolean_param(value):
    if value is None:
        return None
    return str(value).lower() in ('1', 'true', 'on', 'yes')


def list_produto_view(request, id=None):
    produtos = Produto.objects.select_related('categoria', 'fabricante').all()

    busca = request.GET.get('produto', '').strip()
    destaque = _boolean_param(request.GET.get('destaque'))
    promocao = _boolean_param(request.GET.get('promocao'))
    categoria = request.GET.get('categoria', '').strip()
    fabricante = request.GET.get('fabricante', '').strip()
    dias = request.GET.get('dias', '').strip()

    if busca:
        produtos = produtos.filter(produtoo__icontains=busca)
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
    if categoria:
        if categoria.isdigit():
            produtos = produtos.filter(categoria_id=int(categoria))
        else:
            produtos = produtos.filter(categoria__Categoria__iexact=categoria)
    if fabricante:
        if fabricante.isdigit():
            produtos = produtos.filter(fabricante_id=int(fabricante))
        else:
            produtos = produtos.filter(fabricante__fabricante__iexact=fabricante)
    if dias:
        try:
            dias_int = int(dias)
            if dias_int >= 0:
                produtos = produtos.filter(criado_em__gte=timezone.now() - timedelta(days=dias_int))
        except ValueError:
            pass
    if id is not None:
        produtos = produtos.filter(id=id)

    context = {
        'produtos': produtos,
        'categorias': Categoria.objects.all(),
        'fabricantes': Fabricante.objects.all(),
        'filtros': {
            'produto': busca,
            'categoria': categoria,
            'fabricante': fabricante,
        },
    }
    return render(request, 'produto/produto.html', context)


@login_required
def edit_produto_view(request, id):
    produto = get_object_or_404(Produto, id=id)
    context = {
        'produto': produto,
        'fabricantes': Fabricante.objects.all(),
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'produto/produto-edit.html', context)


@login_required
def edit_produto_postback(request):
    if request.method != 'POST':
        return redirect('produtos')

    produto = get_object_or_404(Produto, id=request.POST.get('id'))
    nome = request.POST.get('Produto', '').strip()
    categoria_id = request.POST.get('CategoriaFk')
    fabricante_id = request.POST.get('FabricanteFk')

    if not nome:
        messages.error(request, 'Informe o nome do produto.')
        return redirect('edit_produto', produto.id)

    if not categoria_id or categoria_id == '-1' or not categoria_id.isdigit():
        messages.error(request, 'Selecione uma categoria válida.')
        return redirect('edit_produto', produto.id)
    if not fabricante_id or fabricante_id == '-1' or not fabricante_id.isdigit():
        messages.error(request, 'Selecione um fabricante válido.')
        return redirect('edit_produto', produto.id)

    produto.produtoo = nome
    produto.destaque = request.POST.get('destaque') is not None
    produto.promocao = request.POST.get('promocao') is not None
    produto.msgPromocao = request.POST.get('msgPromocao', '').strip() or None
    produto.categoria = get_object_or_404(Categoria, id=int(categoria_id))
    produto.fabricante = get_object_or_404(Fabricante, id=int(fabricante_id))
    produto.save()
    messages.success(request, 'Produto atualizado com sucesso.')
    return redirect('produtos')


def details_produto_view(request, id):
    produto = get_object_or_404(Produto.objects.select_related('categoria', 'fabricante'), id=id)
    return render(request, 'produto/produto-details.html', {'produto': produto})


@login_required
def delete_produto_view(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produto/produto-delete.html', {'produto': produto})


@login_required
def delete_produto_postback(request):
    if request.method != 'POST':
        return redirect('produtos')
    produto = get_object_or_404(Produto, id=request.POST.get('id'))
    nome = produto.produtoo
    produto.delete()
    messages.success(request, f'Produto "{nome}" excluído com sucesso.')
    return redirect('produtos')


@login_required
def create_produto_view(request):
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()

    if request.method == 'POST':
        nome = request.POST.get('Produto', '').strip()
        categoria_id = request.POST.get('CategoriaFk')
        fabricante_id = request.POST.get('FabricanteFk')
        preco_texto = request.POST.get('preco', '').strip().replace(',', '.')

        if not nome:
            messages.error(request, 'Informe o nome do produto.')
        elif not categoria_id or categoria_id == '-1' or not categoria_id.isdigit():
            messages.error(request, 'Selecione uma categoria válida.')
        elif not fabricante_id or fabricante_id == '-1' or not fabricante_id.isdigit():
            messages.error(request, 'Selecione um fabricante válido.')
        else:
            try:
                preco = Decimal(preco_texto)
                if preco < 0:
                    raise InvalidOperation
            except (InvalidOperation, ValueError):
                messages.error(request, 'Informe um preço válido, por exemplo: 199,90.')
            else:
                produto = Produto(
                    produtoo=nome,
                    destaque=request.POST.get('destaque') is not None,
                    promocao=request.POST.get('promocao') is not None,
                    msgPromocao=request.POST.get('msgPromocao', '').strip() or None,
                    preco=preco,
                    categoria=get_object_or_404(Categoria, id=int(categoria_id)),
                    fabricante=get_object_or_404(Fabricante, id=int(fabricante_id)),
                )
                imagem = request.FILES.get('image')
                if imagem:
                    produto.image = imagem
                produto.save()
                messages.success(request, 'Produto criado com sucesso.')
                return redirect('produtos')

    context = {'fabricantes': fabricantes, 'categorias': categorias}
    return render(request, 'produto/produto-create.html', context)
