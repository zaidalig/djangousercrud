from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import json
from django.shortcuts import render

@csrf_exempt
def user_list_create(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        page_number = request.GET.get('page', 1)

        users = User.objects.filter(username__icontains=query).order_by('id')
        paginator = Paginator(users, 5)  # 5 per page
        page = paginator.get_page(page_number)

        data = list(page.object_list.values('id', 'username', 'email'))
        return JsonResponse({
            'results': data,
            'total_pages': paginator.num_pages,
            'current_page': page.number
        })

    elif request.method == 'POST':
        try:
            payload = json.loads(request.body)
            user = User.objects.create_user(
                username=payload['username'],
                email=payload.get('email', ''),
                password=payload.get('password', '123456')
            )
            return JsonResponse({'id': user.id, 'message': 'User created'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def user_detail_update_delete(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })

    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body)
            user.username = payload.get('username', user.username)
            user.email = payload.get('email', user.email)
            if payload.get('password'):
                user.set_password(payload['password'])
            user.save()
            return JsonResponse({'message': 'User updated'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User deleted'})

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])


def user_crud_page(request):
    return render(request, 'user_crud.html')
