from category.models import Category


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


def current_url(request):
    return {'url':  request.path}
