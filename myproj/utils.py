def handleformerror(form):
    form_errors = []
    if '__all__' in form.errors:
        for error_message in form.errors['__all__']:
            form_errors = error_message
        return form_errors
    else:
        return ''
