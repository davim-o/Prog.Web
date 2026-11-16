from django.shortcuts import render, get_object_or_404, redirect
from loja.models import Produto, Carrinho, CarrinhoItem, Usuario
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def create_carrinhoitem_view(request, produto_id=None):
    produto = get_object_or_404(Produto, pk=produto_id)

    carrinho_id = request.session.get('carrinho_id')
    carrinho = None

    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()

    # Valida se o carrinho existe e se pertence ao dia de hoje
    if not carrinho:
        carrinho = Carrinho.objects.create()
        request.session['carrinho_id'] = carrinho.id
    else:
        hoje = datetime.today().date()
        if carrinho.criado_em.date() != hoje:
            carrinho = Carrinho.objects.create()
            request.session['carrinho_id'] = carrinho.id

    carrinho_item = CarrinhoItem.objects.filter(carrinho=carrinho, produto=produto).first()

    if carrinho_item:
        carrinho_item.quantidade += 1
    else:
        carrinho_item = CarrinhoItem.objects.create(
            carrinho=carrinho,
            produto=produto,
            quantidade=1,
            preco=produto.preco
        )

    carrinho_item.save()
    return redirect('/carrinho')

def list_carrinho_view(request):
    carrinho = None
    carrinho_item = None
    carrinho_id = request.session.get('carrinho_id')

    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        if carrinho:
            carrinho_item = CarrinhoItem.objects.filter(carrinho=carrinho)
        else:
            request.session.pop('carrinho_id', None)

    context = {
        'carrinho': carrinho,
        'itens': carrinho_item
    }

    return render(request, 'carrinho/carrinho-listar.html', context=context)

@login_required
def confirmar_carrinho_view(request):
    carrinho = None
    carrinho_item = None
    carrinho_id = request.session.get('carrinho_id')

    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        if carrinho:
            carrinho_item = list(CarrinhoItem.objects.filter(carrinho=carrinho))
            Usuario.objects.get_or_create(user=request.user)
            carrinho.user = request.user
            carrinho.situacao = 1
            carrinho.confirmado_em = timezone.now()
            carrinho.save()
            request.session.pop('carrinho_id', None)

    context = {
        'carrinho': carrinho,
        'itens': carrinho_item,
    }
    return render(request, 'carrinho/carrinho-confirmado.html', context=context)

def remover_item_view(request, item_id):
    item = get_object_or_404(CarrinhoItem, id=item_id)
    carrinho_id = request.session.get('carrinho_id')

    if item.carrinho and carrinho_id == item.carrinho.id:
        item.delete()
        
    return redirect('/carrinho')

def aumentar_quantidade(request, item_id):
    item = get_object_or_404(CarrinhoItem, id=item_id)
    item.quantidade += 1
    item.save()
    messages.success(request, f'Quantidade de {item.produto.produtoo} aumentada!')
    return redirect('/carrinho')

def diminuir_quantidade(request, item_id):
    item = get_object_or_404(CarrinhoItem, id=item_id)
    if item.quantidade > 1:
        item.quantidade -= 1
        item.save()
        messages.success(request, f'Quantidade de {item.produto.produtoo} reduzida!')
    else:
        messages.warning(request, 'A quantidade mínima é 1. Caso queira remover o item, clique em "Excluir".')
    return redirect('/carrinho')