from django.shortcuts import render
from django.http import HttpResponseBadRequest
from seqtagmodel.text_corrector_cache import get_text_corrector
from website.models import Text, GeneralFeedback


def send_data(request):
    if request.method != 'POST':
        return render(request, 'home.html', {'input': '', 'output': '', 'text_id': -1})

    data_type = request.POST.get('dataType')
    context = {'input': '', 'output': '', 'text_id': -1}

    if data_type == 'sendtext':
        input_string = request.POST.get('input')
        if not input_string:
            input_string = ''

        text_corrector = get_text_corrector()
        final_input_string, final_output_string, str_out = text_corrector.process_text(input_string)

        text_obj = Text.objects.create(
            original_text=final_input_string,
            corrected_text=final_output_string,
            labeled_text=str_out
        )
        context = {'input': input_string, 'output': str_out, 'text_id': text_obj.id}

    elif data_type == 'sendapi':
        feedback = request.POST.get('feedback')
        text_id = request.POST.get('text_id')

        if not (feedback and text_id):
            feedback = 'None'
            text_id = -1
        try:
            text_obj = Text.objects.get(id=text_id)
        except Text.DoesNotExist:
            feedback = 'None'
            text_id = -1
            text_obj = None
            context = {'input': '', 'output': '', 'text_id': -1}
        if text_obj is not None:
            text_obj.feedback = feedback
            text_obj.save()
            context = {'input': text_obj.original_text, 'output': text_obj.labeled_text, 'text_id': text_id}

    elif data_type == 'sendfeedback':
        general_feedback = request.POST.get('gfeedback')
        if not general_feedback:
            general_feedback = 'None'
        GeneralFeedback.objects.create(website_feedback=general_feedback)
    else:
        return HttpResponseBadRequest("Invalid data type.")

    return render(request, 'home.html', context)
