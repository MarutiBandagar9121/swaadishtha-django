from django.shortcuts import render
from django.db.models import Min
from categories.models import Category
from products.models import Product

# Slugs that are "special" categories used for merchandising, not shown in the
# main category grid on the home page.
_SPECIAL_SLUGS = ['featured', 'best-sellers', 'bestsellers', 'new-arrivals']


def _active_published():
    return Product.objects.filter(is_active=True, status=Product.Status.PUBLISHED)


def home(request):
    # Categories shown in the grid (exclude merchandising helpers)
    categories = (
        Category.objects
        .filter(is_active=True)
        .exclude(slug__in=_SPECIAL_SLUGS)
    )

    # Featured products — tagged with the "featured" category slug
    featured_products = (
        _active_published()
        .filter(categories__slug='featured')
        .prefetch_related('images')
        .annotate(min_price=Min('variants__price'))
        .distinct()[:8]
    )

    # Best sellers — tagged with either "best-sellers" or "bestsellers" slug
    bestsellers = (
        _active_published()
        .filter(categories__slug__in=['best-sellers', 'bestsellers'])
        .prefetch_related('images')
        .annotate(min_price=Min('variants__price'))
        .distinct()[:8]
    )

    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'bestsellers': bestsellers,
    })
