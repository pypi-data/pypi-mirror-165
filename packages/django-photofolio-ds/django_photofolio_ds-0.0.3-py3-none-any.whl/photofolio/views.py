from django.shortcuts import render
from util_demian import utils
from .forms import AppointmentForm
from _data import contents


import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)

font_link = "https://fonts.googleapis.com/css2?" \
            "family=Hahmlet:wght@100;200;300;400;500;600;700;800;900&" \
            "family=Noto+Sans+KR:wght@100;300;400;500;700;900&" \
            "family=Noto+Serif+KR:wght@200;300;400;500;600;700;900&" \
            "family=Open+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700;1,800&" \
            "family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&" \
            "family=Cardo:ital,wght@0,400;0,700;1,400&display=swap"


def home(request):
    """
        컨텍스트를 이곳에서 만들지 않고 _data 폴더의 contents.py에서 만들어진 것을 가져다 쓴다.
        """
    c = contents.context

    # _variables.scss에서 한글 폰트를 추가해주고 여기에 적절한 폰트 링크를 적용한다.
    c['font_link'] = font_link
    c['category'] = 'signatures'

    logger.info(c)
    return render(request, 'photofolio/index.html', c)


def about(request):
    c = contents.context

    # _variables.scss에서 한글 폰트를 추가해주고 여기에 적절한 폰트 링크를 적용한다.
    c['font_link'] = font_link

    logger.info(c)

    return render(request, 'photofolio/sub/about.html', c)


def contact(request):
    c = contents.context

    # _variables.scss에서 한글 폰트를 추가해주고 여기에 적절한 폰트 링크를 적용한다.
    c['font_link'] = font_link

    logger.info(c)

    return render(request, 'photofolio/sub/contact.html', c)


def gallery(request, category):
    c = contents.context

    # _variables.scss에서 한글 폰트를 추가해주고 여기에 적절한 폰트 링크를 적용한다.
    c['font_link'] = font_link
    c['category'] = category

    for item in c['gallery']:
        if item[0] == c['category']:
            subtitle = item[1]
            break
    c['subtitle'] = subtitle

    logger.info(c)

    return render(request, 'photofolio/sub/gallery.html', c)


def services(request):
    c = contents.context

    # _variables.scss에서 한글 폰트를 추가해주고 여기에 적절한 폰트 링크를 적용한다.
    c['font_link'] = font_link

    logger.info(c)

    return render(request, 'photofolio/sub/services.html', c)

