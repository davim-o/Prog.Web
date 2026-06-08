from django.shortcuts import render, redirect
from loja.models import Produto, Fabricante, Categoria
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage


def list_produto_view(request, id=None):

    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")

    produtos = Produto.objects.all()

    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)

    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)

    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)

    if categoria is not None:
        produtos = produtos.filter(categoria__Categoria=categoria)

    if fabricante is not None:
        produtos = produtos.filter(fabricante__Fabricante=fabricante)

    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days=int(dias))
        produtos = produtos.filter(criado_em__gte=now)

    context = {
        'produtos': produtos
    }

    return render(
        request,
        template_name='produto/produto.html',
        context=context,
        status=200
    )


def edit_produto_view(request, id=None):

    produtos = Produto.objects.all()

    if id is not None:
        produtos = produtos.filter(id=id)

    produto = produtos.first()
    print(produto)

    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()

    context = {
        'produto': produto
    }

    return render(
        request,
        template_name='produto/produto-edit.html',
        context=context,
        status=200
    )


def edit_produto_postback(request, id=None):

    if request.method == 'POST':

        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")

        try:

            obj_produto = Produto.objects.filter(id=id).first()

            if obj_produto is not None:

                obj_produto.Produto = produto
                obj_produto.destaque = (destaque is not None)
                obj_produto.promocao = (promocao is not None)
                obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
                obj_produto.categoria = Categoria.objects.filter(id=categoria).first()

                if msgPromocao is not None:
                    obj_produto.msgPromocao = msgPromocao

                obj_produto.save()

                print("Produto %s salvo com sucesso" % produto)

        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)

    return redirect('/produto')

def details_produto_view(request, id=None):

    produtos = Produto.objects.all()

    if id is not None:
        produtos = produtos.filter(id=id)

    produto = produtos.first()

    print(produto)

    context = {
        'produto': produto
    }

    return render(
        request,
        template_name='produto/produto-details.html',
        context=context,
        status=200
    )

def delete_produto_view(request, id=None):
    # Processa o evento GET gerado pela action
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    context = {'produto': produto}
    return render(request, template_name='produto/produto-delete.html', context=context, status=200)


# adicione a função que trata o postback da interface de exclusão
def delete_produto_postback(request, id=None):
    # Processa o post back gerado pela action
    if request.method == 'POST':
        # Salva dados editados
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        print("postback-delete")
        print(id)
        try:
            Produto.objects.filter(id=id).delete()
            print("Produto %s excluido com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
        return redirect("/produto")
    
def create_produto_view(request, id=None):
    if request.method == 'POST':
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")
        
        # Coleta os IDs selecionados no HTML
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")
        
        # Criação do objeto
        obj_produto = Produto()
        obj_produto.Produto = produto
        obj_produto.destaque = (destaque is not None)
        obj_produto.promocao = (promocao is not None)
        
        if msgPromocao is not None:
            obj_produto.msgPromocao = msgPromocao
            
        obj_produto.preco = 0
        if (preco is not None) and (preco != ""):
            # CORREÇÃO: Troca a vírgula por ponto para o banco de dados aceitar
            preco_limpo = preco.replace(',', '.')
            obj_produto.preco = preco_limpo
            
        # Vincula a Categoria e o Fabricante se forem selecionados
        if categoria_id and categoria_id != "-1":
            obj_produto.categoria_id = categoria_id
        if fabricante_id and fabricante_id != "-1":
            obj_produto.fabricante_id = fabricante_id
            
        obj_produto.criado_em = timezone.now()
        obj_produto.alterado_em = obj_produto.criado_em
        
        # Upload da imagem
        if request.FILES.get('image'):
            imagefile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(imagefile.name, imagefile)
            if filename:
                obj_produto.image = filename
                
        # Salvando no banco de dados
        obj_produto.save()
        
        return redirect("/produto")
        
    context = {
        'categorias': Categoria.objects.all(),
        'fabricantes': Fabricante.objects.all()
    }
    return render(request, template_name='produto/produto-create.html', context=context, status=200)