
def process_form(request, Form, instance, prefix=None):
    if request.method == 'POST':
        values = request.POST.copy()
        form = Form(values, instance=instance, prefix=prefix)
        
        if form.is_valid():
            object=form.save()
            return True
        else:
            form_error(request, form)
    else:
        form = Form()
