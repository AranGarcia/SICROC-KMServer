from django.http import HttpResponse

def index(request):
    text = b'''
    <html>
        <head>
            <title>Complain centers</title>
        </head>
        <body>
            <h1>K-Means Server</h1>

            <p>
                El servicio se encuentra en <b>/centers</b>.
            </p>
        </body>
    </html>
    '''
    return HttpResponse(text)