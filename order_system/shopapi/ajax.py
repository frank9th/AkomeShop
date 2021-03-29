from dajaxice.utils import deserialize_form 
from staffs.forms import ContactForm
from dajax.core import Dajax
from staffs.models import Contact

@dajaxice_register
def send_form(request, form):
	dajax = Dajax()
	form = AddClientForm(deserialize_form(form))

	if form.is_valid():
		dajax.remove_css_class('#client_form', 'error')
		cl = Client()
		cl