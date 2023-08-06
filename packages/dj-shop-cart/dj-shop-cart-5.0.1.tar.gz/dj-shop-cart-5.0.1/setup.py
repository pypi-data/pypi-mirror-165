# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_shop_cart', 'dj_shop_cart.migrations', 'migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0', 'attrs>=21.4,<23.0']

setup_kwargs = {
    'name': 'dj-shop-cart',
    'version': '5.0.1',
    'description': 'Simple django cart manager for your django projects.',
    'long_description': '# dj-shop-cart\n\nA simple and flexible cart manager for your django projects.\n\n[![pypi](https://badge.fury.io/py/dj-shop-cart.svg)](https://pypi.org/project/dj-shop-cart/)\n[![python](https://img.shields.io/pypi/pyversions/dj-shop-cart)](https://github.com/Tobi-De/dj-shop-cart)\n[![django](https://img.shields.io/pypi/djversions/dj-shop-cart)](https://github.com/Tobi-De/dj-shop-cart)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/dj-shop-cart/blob/master/LICENSE)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n✨📚✨ [Read the full documentation](https://tobi-de.github.io/dj-shop-cart/)\n\n## Features\n\n- Add, remove, decrement and clear items from cart\n- Authenticated users cart can be saved to database\n- Write custom methods to easily hook into the items add / remove flow\n- Custom **get_price** method to ensure that the cart always have an up-to-date products price\n- Each item in the cart hold a reference to the associated product\n- Metadata data can be attached to cart items\n- Supports specification of product variation details\n- Available context processor for easy access to the user cart in all your django templates\n- Swappable backend storage, with session and database provided by default\n\n\n## Installation\n\nInstall **dj-shop-cart** with pip or poetry.\n\n```bash\n  pip install dj-shop-cart\n```\n\n## Quickstart\n\n```python3\n\n# settings.py\n\nTEMPLATES = [\n    {\n        "OPTIONS": {\n            "context_processors": [\n                ...,\n                "dj_shop_cart.context_processors.cart", # If you want access to the cart instance in all templates\n            ],\n        },\n    }\n]\n\n# models.py\n\nfrom django.db import models\nfrom dj_shop_cart.cart import CartItem\nfrom decimal import Decimal\n\nclass Product(models.Model):\n    ...\n\n    def get_price(self, item:CartItem)->Decimal:\n        """The only requirements of the dj_shop_cart package apart from the fact that the products you add\n        to the cart must be instances of django based models. You can use a different name for this method\n        but be sure to update the corresponding setting (see Configuration). Even if you change the name the\n        function signature should match this one.\n        """\n\n\n# views.py\n\nfrom dj_shop_cart.cart import get_cart_class\nfrom django.http import HttpRequest\nfrom django.views.decorators.http import require_POST\nfrom django.shortcuts import get_object_or_404\n\nfrom .models import Product\n\nCart = get_cart_class()\n\n\n@require_POST\ndef add_product(request: HttpRequest, product_id:int):\n    product = get_object_or_404(Product.objects.all(), pk=product_id)\n    quantity = int(request.POST.get("quantity"))\n    cart = Cart.new(request)\n    cart.add(product, quantity=quantity)\n    ...\n\n\n@require_POST\ndef remove_product(request: HttpRequest):\n    item_id = request.POST.get("item_id")\n    quantity = int(request.POST.get("quantity"))\n    cart = Cart.new(request)\n    cart.remove(item_id=item_id, quantity=quantity)\n    ...\n\n\n@require_POST\ndef empty_cart(request: HttpRequest):\n    Cart.new(request).empty()\n    ...\n\n```\n\n## Used By\n\nThis project is used by the following companies:\n\n- [Fêmy bien être](https://www.femybienetre.com/)\n\n## Development\n\nPoetry is required (not really, you can set up the environment however you want and install the requirements\nmanually) to set up a virtualenv, install it then run the following:\n\n```sh\npoetry install\npre-commit install --install-hooks\n```\n\nTests can then be run quickly in that environment:\n\n```sh\npytest\n```\n\n## Feedback\n\nIf you have any feedback, please reach out to me at degnonfrancis@gmail.com\n\n## Credits\n\nThanks to [Jetbrains](https://jb.gg/OpenSource) for providing an Open Source license for this project.\n\n<img height="200" src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.png" alt="JetBrains Logo (Main) logo.">\n',
    'author': 'Tobi DEGNON',
    'author_email': 'tobidegnon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tobi-De/dj-shop-cart',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
