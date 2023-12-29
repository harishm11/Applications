def handleformerror(form):
    form_errors = []

    # Handle form-specific errors
    if '__all__' in form.errors:
        for error_message in form.errors['__all__']:
            form_errors.append(error_message)

    # Handle non-form errors
    if hasattr(form, 'non_form_errors') and callable(getattr(form, 'non_form_errors')):
        non_form_errors = form.non_form_errors()
        if non_form_errors:
            form_errors.extend(non_form_errors)
    if form_errors == []:
        return ''
    else:
        return form_errors
