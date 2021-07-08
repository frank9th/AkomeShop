
from .models import Category 

def menu_category(request):
	# this returs all the objects except the service category 
	categories = Category.objects.exclude(name='Services')

	return {'menu_categories':categories}
