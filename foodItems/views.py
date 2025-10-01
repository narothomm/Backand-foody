from django.http import JsonResponse
from . models import FoodItem
from django . forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger,Paginator

#get data with image
# def get_food_items(request):
#     food_items = FoodItem.objects.all()
#     data = []
#     for item in food_items:
#         item_dict = model_to_dict(item)
#         if item.image:
#             item_dict['image']=request.build_absolute_uri(item.image.url)
#         else:
#             item_dict['image']=None
#         data.append(item_dict)
#     return JsonResponse(data, safe=False)


def get_food_items(request):
    try:
        # Query parameters
        page_number=request.GET.get('page',1)
        print(page_number)
        page_size=request.GET.get('page_size',6)
        
        # Page size validation
        try:
            page_size=int(page_size)
            if page_size<=0:
                raise ValueError
        except ValueError:
            return JsonResponse({"error":"Invalid page size,page size must be an integer"},status=400)
        
        # Get food items
        food_items=FoodItem.objects.all().order_by("id")
        
        # Pagination
        paginator=Paginator(food_items,page_size)
        
        try:
            page_obj=paginator.get_page(page_number)
        except PageNotAnInteger:
            return JsonResponse({"error":"Invalid page number,page number must be an integer"},status=400)
        
        # Convert to dict
        data=[]
        for item in page_obj.object_list:
            item_dict=model_to_dict(item)
            
            # নিশ্চিতভাবে ID পাঠানো
            item_dict['id'] = item.id
            
            # Image URL যোগ করা
            if item.image:
                item_dict['image']=request.build_absolute_uri(item.image.url)
            else:
                item_dict['image']=None
            data.append(item_dict)
            
        return JsonResponse({
            "count": paginator.count,            
            "current_page": int(page_number),    
            "num_of_pages": paginator.num_pages, 
            "result": data                        # এই পেজের ডেটা
        })     
    except Exception:
        return JsonResponse({"error":"an unexcepted error occured"},status=500)        
                
        
        

@csrf_exempt
def add_food_item(request):
    if request.method=="POST":
        try:
            title=request.POST.get('title')
            description=request.POST.get('description')
            price=request.POST.get('price')
            quantity=request.POST.get('quantity')
            origin=request.POST.get('origin')
            category=request.POST.get('category')
            image=request.FILES.get('image')
        
            food=FoodItem.objects.create(
                title=title,
                price=price,
                description=description,
                quantity=quantity,
                origin=origin,
                category=category,
                image=image
            )
       
            return JsonResponse({ 'message':"food item added successfully"})
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
    return JsonResponse({'error':"invalid request method"},status=405)
        
        
@csrf_exempt
def update_food_item(request,item_id):
    if request.method =="POST":
        try:
            food = FoodItem.objects.get(id=item_id)
            food.title = request.POST.get('title',food.title)
            food.description = request.POST.get('description',food.description)
            food.price = request.POST.get('price',food.price)
            food.quantity = request.POST.get('quantity',food.quantity)
            food.origin = request.POST.get('origin',food.origin)
            food.category = request.POST.get('category',food.category)
            
            if 'image' in request.FILES:
                food.image = request.FILES['image']
            food.save()
            return JsonResponse({'message':'Food item updated successfully'})
        except FoodItem.DoesNotExist:
            return JsonResponse({"message":"food item not found"},status = 404)
        except Exception as e:
            return JsonResponse({"error":str(e)},status = 405)
    return JsonResponse({"error":"only post method is allowed"},status = 405)


def get_single_food_item(request,item_id):
    if request.method=="GET":
        try:
            food_odj=FoodItem.objects.get(id=item_id)
            food = model_to_dict(food_odj)
            if food_odj.image:
                food['image']=request.build_absolute_uri(food_odj.image.url)
            else:
                food['image']=None
                
            return JsonResponse(food)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=400)
        except FoodItem.DoesNotExist:
            return JsonResponse({'error':"Food item not found"},status=404)
    return JsonResponse({"error":"Only get method is allowed"},status=405)


@csrf_exempt
def delete_food_item(request,item_id):
    if(request.method=="DELETE"):
        try:
            food=FoodItem.objects.get(id=item_id)
            food.delete()
            return JsonResponse({"message":"food item delete successfully "},status=200)
        except FoodItem .DoesNotExist:
            return JsonResponse({"message":"food item not found "},status=404)
    return JsonResponse({"message":"Only get method is allod"},status=405)  



def get_popular_foods(request):
    if request.method == "GET":
        try:
            food_items = FoodItem.objects.filter(rating__gte=4.5).order_by('-rating')[:6]
            
            data = []
            for item in food_items:
                item_dict = model_to_dict(item)
                #if item.image:
                item_dict['image'] = request.build_absolute_uri(item.image.url) if item.image else None
                data.append(item_dict)

            return JsonResponse(data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({"error": "Only GET method is allowed"}, status=405)  



def get_foods_by_category(request):
    if(request.method=="GET"):
        category=request.GET.get('category')
        
        try:
            food_items=FoodItem.objects.filter(category__iexact=category)
            data=[]
            
            for item in food_items:
                item_dict=model_to_dict(item)
                item_dict['image']=request.build_absolute_uri(item.image.url) if item.image else None 
                data.append(item_dict) 
                
            return JsonResponse(data,safe=False)
        except Exception as e:
            return JsonResponse({'error':str(e)}, status=400)
    return JsonResponse({'error':"Only get method is allod "},status=405)
     
                  
     
                 
              

