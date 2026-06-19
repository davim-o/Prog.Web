from django.shortcuts import render, redirect
from loja.models import Produto, Fabricante, Categoria
from datetime import timedelta
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

    context = {
        'produto': produto,
        'categorias': Categoria.objects.all(),
        'fabricantes': Fabricante.objects.all()
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

                obj_produto.fabricante = Fabricante.objects.filter(
                    id=fabricante
                ).first()

                obj_produto.categoria = Categoria.objects.filter(
                    id=categoria
                ).first()

                if msgPromocao is not None:
                    obj_produto.msgPromocao = msgPromocao

                if request.FILES.get('image'):

                    if obj_produto.image:
                        obj_produto.image.delete(save=False)

                    imagefile = request.FILES['image']

                    fs = FileSystemStorage()
                    filename = fs.save(imagefile.name, imagefile)

                    if filename:
                        obj_produto.image = filename

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

    produtos = Produto.objects.all()

    if id is not None:
        produtos = produtos.filter(id=id)

    produto = produtos.first()

    context = {
        'produto': produto
    }

    return render(
        request,
        template_name='produto/produto-delete.html',
        context=context,
        status=200
    )


def delete_produto_postback(request, id=None):

    if request.method == 'POST':

        id = request.POST.get("id")
        produto = request.POST.get("Produto")

        try:

            obj_produto = Produto.objects.filter(id=id).first()

            if obj_produto is not None:

                if obj_produto.image:
                    obj_produto.image.delete(save=False)

                obj_produto.delete()

            print("Produto %s excluido com sucesso" % produto)

        except Exception as e:
            print("Erro excluindo produto: %s" % e)

    return redirect("/produto")


def create_produto_view(request, id=None):

    if request.method == 'POST':

        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")

        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")

        obj_produto = Produto()

        obj_produto.Produto = produto
        obj_produto.destaque = (destaque is not None)
        obj_produto.promocao = (promocao is not None)

        if msgPromocao is not None:
            obj_produto.msgPromocao = msgPromocao

        obj_produto.preco = 0

        if preco is not None and preco != "":
            obj_produto.preco = preco.replace(',', '.')

        if categoria_id and categoria_id != "-1":
            obj_produto.categoria_id = categoria_id

        if fabricante_id and fabricante_id != "-1":
            obj_produto.fabricante_id = fabricante_id

        if request.FILES.get('image'):

            imagefile = request.FILES['image']

            fs = FileSystemStorage()
            filename = fs.save(imagefile.name, imagefile)

            if filename:
                obj_produto.image = filename

        obj_produto.save()

        return redirect("/produto")

    context = {
        'categorias': Categoria.objects.all(),
        'fabricantes': Fabricante.objects.all()
    }

    return render(
        request,
        template_name='produto/produto-create.html',
        context=context,
        status=200
    )