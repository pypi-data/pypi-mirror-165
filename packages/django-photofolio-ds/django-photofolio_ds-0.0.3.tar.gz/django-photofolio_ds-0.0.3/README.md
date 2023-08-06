# django-photofolio_ds

django-photofolio_ds 는 photofolio-pro v4.8.0을 장고에 맞게 포팅한 장고앱이다.


> 프로젝트에 설치하기
> 1. photofolio 앱을 프로젝트 settings.py 의 INSTALLED_APPS 에 추가한다.
> ```python
> import os
> INSTALLED_APPS = [
>     ...
>     'photofolio',
> ]
> ```
> 2. 프로젝트의 urls.py에 photofolio url을 추가한다.
> ```python
> from django.urls import path, include
> 
> urlpatterns = [
>     ...
>     path('', include('photofolio.urls')),
> ]
> ```
> 3. 케이스를 입력하기 위해서 프로젝트에 photofolio 데이터베이스를 생성한다.
> ```commandline
>     python manage.py makemigrations photofolio
>     python manage.py migrate
>     python manage.py createsuperuser
> ```
> 4. http://127.0.0.1:8000/admin 으로 접속하여 블로그를 입력한다.

> 프로젝트 구조 생성하기
> 1. 개별 업체만의 static 폴더 경로를 INSTALLED_APPS 에 추가한다.
> ```python
> import os
> STATICFILES_DIRS = [
>   os.path.join(BASE_DIR, '_static/'),
> ]
> ```
> 2. _data 폴더를 생성하고 contents.py내에 데이터를 형식에 맞게 입력한다.
> 3. _static 폴더를 생성하고 각종 이미지 등을 형식에 맞게 저장한다.

> 참고 : SCSS 설치하기 - 프로젝트에 SCSS를 설치해야 앱이 작동한다.    
> https://www.accordbox.com/blog/how-use-scss-sass-your-django-project-python-way/   
> 1. django_compressor, django-libsass를 설치한다. (앱을 설치하면 자동으로 설치된다.)
> ```commandline
> pip install django_compressor django-libsass
> ```
> 2. 프로젝트 settings.py 의 INSTALLED_APPS 에 다음을 추가한다.
> ```python
> import os
> INSTALLED_APPS = [
>     ...
>     'compressor',
> ]
> 
> COMPRESS_PRECOMPILERS = (
>     ('text/x-scss', 'django_libsass.SassCompiler'),
> )
> 
> STATICFILES_FINDERS = [
>     'django.contrib.staticfiles.finders.FileSystemFinder',
>     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
>     'compressor.finders.CompressorFinder',
> ]
> 
> # compressor 앱을 실행하기 위해서는 STATIC_ROOT가 설정되어 있어야 한다.
> STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
> ```
