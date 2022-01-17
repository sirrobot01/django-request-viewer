# Django Request Viewer


Log and view requests and exceptions made on your Django App

#### Updates 17th, January 2022

- Adds Exception logger
- Cleaned up the code

### Introduction


<img width="1440" alt="Screenshot 2021-03-29 at 09 30 17" src="https://user-images.githubusercontent.com/32229538/112814802-8f9ef780-9077-11eb-9d4c-0d2c4a394c6b.png">


Recently, [@ichtrojan](https://github.com/ichtrojan) and [@toniastro](https://github.com/toniastro) released [horus](https://github.com/ichtrojan/horus), a request logger and viewer for Go. Then I felt the need for something like that for the Django community.

### Installation

Install using pip

```bash
pip install django-request-viewer
```

### Usage


Add `'request-viewer'` to your `INSTALLED_APPS` in settings.py.

    INSTALLED_APPS = [
        ...
        'request_viewer',
        ...
    ]
  
  
Add  `'request_viewer.middleware.RequestViewerMiddleware'` to your MIDDLEWARE list in settings.py.

    MIDDLEWARE = [
        ...
        'request_viewer.middleware.RequestViewerMiddleware',
        ...
    ]  

##### To log exceptions, add

Add  `'request_viewer.middleware.ExceptionMiddleware'` to your MIDDLEWARE list in settings.py.

    MIDDLEWARE = [
        ...
        'request_viewer.middleware.ExceptionMiddleware',
        ...
    ]  
    
Add `'request-viewer'` to your main urls.py

    urlpatterns = [
      ...
      path('logs/', include('request_viewer.urls'))
      ...
    ]
    
Run migrations, `python manage.py migrate request-viewer`
    
**OPTIONAL** 

Add `REQUEST_VIEWER` dictionary to your settings.py. 


**LIVE_MONITORING**: Default: `True`, False to pause monitoring. 

**WHITELISTED_PATH**: Default: `[]`, This is a list of paths to be excluded when monitoring

    {
      "LIVE_MONITORING": True,
      "WHITELISTED_PATH": ['admin/']
    }
  
**Note**: Media url, Static url and request-viewer url are automatically excluded.
<br>

### Start your server and head to http://localhost:8000/log/request-viewer to view requests

### Head to http://localhost:8000/log/request-viewer/exceptions to view exceptions


View your request logs.<br> 

<img width="1440" alt="Screenshot 2021-03-29 at 09 30 33" src="https://user-images.githubusercontent.com/32229538/112814936-b3623d80-9077-11eb-9cdf-38f7088b6a24.png">

### Contribute

Well, no big drama, fork the repo and make pull requests, easy-peasy, right?

### TODO
* JSON export
* Caching
* Create an African unicorn
* Buy a yacht

### Credits

* Toni Akinmolayan - [twitter](https://twitter.com/toniastro_) [GitHub](https://github.com/toniastro)
* Michael Trojan Okoh - [twitter](https://twitter.com/ichtrojan) [GitHub](https://github.com/ichtrojan)



### Follow me (I am not boring, I promise)
* [Twitter](https://twitter.com/sirrobot01)
* [Github](https://github.com/sirrobot01)




