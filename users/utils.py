from .models import CustomUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def developer_search(request):
    '''
    search developer model for records matching 
    query string
    '''
    q = request.GET.get("search_query", '')
    result =\
        CustomUser.search.search(q_string=q) if q else CustomUser.objects.all()
    context = {
        "users": result,
        "q": q
    }
    return context


def paginate(request, result_count, q_set):
    '''
    returns paginated query_set and custom paginator range
    '''
    try:
        page_number = int(request.GET.get('page'))
    except:
        page_number = 1

    pages = Paginator(q_set, result_count)
    # if not isinstance(page_number, int):
    #     print("Nada bruv")
    try:
        query_set = pages.page(page_number)
    except EmptyPage:
        page_number = pages.num_pages
        query_set = pages.page(page_number)

    if page_number - 2 < 1:
        left_index = 1
    else:
        left_index = page_number - 2

    if page_number + 3 > pages.num_pages:
        right_index = pages.num_pages + 1
    else:
        right_index = page_number + 3

    custom_range = range(left_index, right_index)
    # print(custom_range, left_index, right_index)
    return query_set, custom_range