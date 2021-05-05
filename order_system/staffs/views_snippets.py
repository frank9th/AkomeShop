

def get_client_code(request, code):	
	try:
		client_code = Client.objects.get(client_code=code)
		messages.success(request, "The User is doing Great")
		return client_code 
	except ObjectDoesNotExist:
		#agent_code = {}
		messages.warning(request, "Enter a valid user code ")
		return redirect('/')

def get_agent_code(request, code):	
	try:
		agent_code = Agent.objects.get(agent_code=code)
		messages.success(request, "The Agent is actually well feed")
		return agent_code 
	except ObjectDoesNotExist:
		#agent_code = {}
		messages.warning(request, "Enter a valid agent code ")
		return redirect('/')



def addClient(request):
	code = request.POST.get('code')
	client = get_client_code(request, code)
	form = AddClientForm( request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			try:

				title= form.cleaned_data.get('title')
				full_name=form.cleaned_data.get('full_name')
				phone1=form.cleaned_data.get('phone1')
				phone2=form.cleaned_data.get('phone2')
				email= form.cleaned_data.get('email')
				agent_code= form.cleaned_data.get('agent_code')
				land_mark= form.cleaned_data.get('land_mark')
				town = form.cleaned_data.get('town')
				sex = form.cleaned_data.get('sex')
				apartment_address=form.cleaned_data.get('apartment_address')
				client_code = create_unique_code()
			
				client_details= Client(
					title= title,
					full_name = full_name,
					email = email,
					phone1 = phone1,
					phone2 = phone2,
					town = town,
					apartment_address = apartment_address,
					client_code = client_code,
					agent_code = agent_code
					)	

				client_details.save()
				messages.success(request, title  +  full_name +  " registerd successully client's code is: " + client_code )
				return redirect('/profile')
				# TODO: Send Code as SMS TO CLIENT 
			except ObjectDoesNotExist:
				messages.info(request, "The Client already exist ")				
	context={
	'form':form, 
	'client':client,
	#'agent_form':CodeForm(),
	}
	return render(request, 'user_account/add_client.html', context)

def addVendor(request):
	code = request.POST.get('code')
	client = get_client_code(request, code)
	#agent = get_agent_code(request, code)

	try:
		clientId = Client.objects.get(id=request.POST.get('clientId'))
		agentId = Agent.objects.get(id=request.POST.get('agentId'))
	except Exception as e:
		pass

	form = AddVendorForm(request.POST or None )
	if request.method == 'POST':
		if form.is_valid():
			business_name = form.cleaned_data.get('business_name')
			product_name = form.cleaned_data.get('product_name')
			goods = form.cleaned_data.get('goods')
			services = form.cleaned_data.get('services')
			skill = form.cleaned_data.get('skill')
			agent_code = form.cleaned_data.get('agent_code')
			try:
				agent = Agent.objects.get(id=request.POST.get(agent_code))
			except Exception as e:
				pass

			vendor_code = create_unique_code()
			vendor_details = Vendor(
				info = clientId,
				business_name = business_name, 
				product_name = product_name, 
				goods = goods, 
				services = services, 
				skill = skill, 
				vendor_code = vendor_code,
				#agent_code= agent,
				)
			vendor_details.save()
			messages.success(request, " registerd successully vendor's code is:" + vendor_code )
			
			# TODO: Send Code as SMS TO VENDOR 
			return redirect('/profile')

	context={'form':form, 
	'client':client,
	#'agent': agent
	}
	return render(request, 'user_account/add_vendor.html', context)

def addAgent(request):
	code = request.POST.get('code')
	client = get_client_code(request, code)
	try:
		clientId = Client.objects.get(id=request.POST.get('clientId'))
		agentId = Agent.objects.get(id=request.POST.get('agentId'))
	except Exception as e:
		pass

	form = AddAgentForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			zone = form.cleaned_data.get('zone')
			bike = form.cleaned_data.get('bike')
			keke = form.cleaned_data.get('keke')
			car = form.cleaned_data.get('car')
			agent_type = form.cleaned_data.get('agent_type')
			agent_code = create_unique_code()
			#codebox = Codebox(code=agent_code, name=full_name)
			#codebox.save()
			agent_details = Agent(
				info = clientId,
				zone = zone,
				bike = bike, 
				keke = keke,
				car = car,
				agent_type= agent_type,
				agent_code=agent_code
				)
			#agent_details.agent_code = codebox
			agent_details.save()
			messages.success( request, " Agent added succesfully. Agent code:" + agent_code )
			# TODO: SEND CODE 
			return redirect('/profile')

	context={'form':form, 'client':client}
	return render(request, 'user_account/add_agent.html', context)