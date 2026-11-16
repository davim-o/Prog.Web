from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from loja.models import Produto, Favorito
from django.shortcuts import render


@login_required
def favoritar_view(request, produto_id):
    produto = Produto.objects.filter(id=produto_id).first()
    if not produto:
        messages.error(request, 'Produto não encontrado.')
        return redirect('home')

    favorito, created = Favorito.objects.get_or_create(user=request.user, produto=produto)
    if created:
        messages.success(request, f'"{produto.produtoo}" adicionado aos favoritos!')
    else:
        favorito.delete()
        messages.info(request, f'"{produto.produtoo}" removido dos favoritos.')

    # Volta para a página de onde veio (home ou onde o botão foi clicado)
    next_url = request.GET.get('next', '/')
    return redirect(next_url)


@login_required
def lista_favoritos_view(request):
    favoritos = Favorito.objects.filter(user=request.user).select_related('produto')
    context = {'favoritos': favoritos}
    return render(request, 'favorito/favorito-listar.html', context=context)
