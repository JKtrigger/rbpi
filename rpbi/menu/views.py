# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re
from datetime import datetime

from django.contrib.auth import login
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.helpers import list_day_from_monday_till_friday
from core.models import BaseRBPIUser, Office
from core.tasks import send_email
from menu.models import Order, DisableDateOrder


# todo: Перевести все VIEW и Json.Parse

@csrf_exempt
def send_login(request):
    post = request.POST
    return HttpResponse(
        json.dumps(
            {
                'error': 'unsuccessfully',
                'details':
                    """You need to log in <br>
                    <form action="/login" method='post' id="ModalForm">
                        <div class="form-group">
                            <label for="pwd">Password:</label>
                            <input 
                                type="password" 
                                class="form-control" 
                                id="pwd"
                                name="password"
                                >
                            <label for="username">Username:</label>
                            <input 
                                type="text" 
                                class="form-control" 
                                id="username"
                                name="username"
                                value={}
                                >
                            <input 
                                value={} 
                                name="csrfmiddlewaretoken"
                                hidden    
                            >

                        </div>
                        <button 
                            type="button" 
                            class="btn btn-default"
                            onclick="modalSubmit()"
                            >
                        Submit
                        </button>

                    </form>
                    <script>
                        {}
                    </script>

                    """.format(
                        post.get('user'),
                        post.get('csrfmiddlewaretoken'),
                        """
        /*
            вызывается при клике по кнопке submit модального окна
        */
        function modalSubmit(){
            var input = $('#ModalForm').find('input');

            data = {}
            for (i = 0; i < input.length; i++ ) {
                var current = $(input[i]) ;
                var name = current.attr('name');
                var value = current.val();
                data[name] = value

            }
            $.ajax({
                url : '/login',
                type : "POST",
                data : data,
                success : function(json) {
                    console.log(json)
                    if (json.error){
                        var default_text = "Some Error on Server";
                        $("h4.modal-title").text(
                            json.head || default_text);
                        $("div.modal-body>p").html(
                        json.error +"<br>"+json.details
                        )

                    }
                    else{
                        $("h4.modal-title").text("Well done!");
                        $("div.modal-body>p").text(
                            json.success
                        )
                    }
                },
                error : function(xhr,errmsg,err) {
                    $("h4.modal-title").text("Request Error");
                        $("div.modal-body>p").text(
                            xhr.status + ": " + xhr.responseText
                        )
                }
             });
        }
                        """
                    )
                ,
                'head': 'Permission'
            }
        ),
        content_type="application/json"
    )


@csrf_exempt
def login_in(request):
    user = request.POST.get('username')
    password = request.POST.get('password')
    users = BaseRBPIUser.objects_active_users.filter(
        username=user).filter(password=password)
    if users.exists():
        try:
            user = users.get()
        except user.multipleobjectsreturned:
            # TODO : Сделалать обработку сообщений exceptions 
            message = {'error': 'Multiple objects return !'}
        else:
            message = {'success': 'Now you can submit you order!'}
            login(request, user)
    else:
        message = {'error': 'not valid user or password'}
    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )


@csrf_exempt
def submit_order(request):
    post = request.POST
    if request.user.username != post.get('user', -1):
        return send_login(request)
    orders = {}
    for key in post.keys():

        value = post.get(key)

        option = re.compile(
            '((?P<option_menu>[a-z]{5,6})_)?(?P<date>\d{4}-\d{2}-\d{2})'
        )
        result = option.match(key)
        # собираем данные перед сабминитом

        if result:
            option_menu = result.group('option_menu') or 'place'
            # todo : ОПРЕДЕЛИТСЯ СО СТРАНДАРТОМ
            # где то предаю , где то не передаю
            option_menu = option_menu.replace('group', 'place')
            date = result.group('date')

            if option_menu == 'count':

                if orders.get(date, None):
                    orders[date].update({
                        'first': value or 0,
                        'second': value or 0,
                        'salad': value or 0,
                    })
                else:
                    if option_menu is 'place':
                        orders[date] = {option_menu: value or 0}
                        continue
                    orders[date] = {
                        'first': value or 0,
                        'second': value or 0,
                        'salad': value or 0,
                    }
                continue
            if orders.get(date, None):
                orders[date].update({option_menu: value or 0})
            else:
                orders[date] = {option_menu: value or 0}

    list_to_save_orders = []
    disabled_dates = map(
        lambda x: x.isoformat(),
        list(
            DisableDateOrder.objects.filter(
                disabled_date__in=orders.keys()
            ).values_list(
                'disabled_date', flat=True)
        )
    )
    message = ''
    for order in orders:
        if order in disabled_dates:
            # FIXME: выполняется в цикле
            message = {'success': u'lunches successfully ordered, \n\n\n\nbut'
                                  u' some of dates are ignored {} '
                                  u' any order changes '.format(disabled_dates)
                       }
            continue
        if orders.get(order, {}).get('place', None):
            # если задано место, даже без обеда
            # то сохраняем заказ
            # Нужно для отмены заказа
            Order.objects.filter(
                customer=request.user,
                order_date=order,
            ).delete()

            options_to_save = {
                'customer': request.user,
                'user_modifier': request.user,
                'order_date': order,
                'office': Office.objects_active_offices.get(
                    name=orders.get(order, {}).get('place')
                ),
                'first_course': orders.get(order, {}).get('first'),
                'second_course': orders.get(order, {}).get('second'),
                'salad': orders.get(order, {}).get('salad'),
            }

            list_to_save_orders.append(Order(**options_to_save))

    message = message or {'success': u'lunches successfully ordered'}

    try:
        # fixme: list_to_save = [] ?
        Order.objects.bulk_create(list_to_save_orders)
    except Exception as err:
        message = {'error': 'unsuccessfully', 'details': err}
        #  TODO : logger
    else:
        user = BaseRBPIUser.objects_active_users.get(username=request.user)
        send_email.delay(
            user.email, 'Your order received successfully', 'Order changes'
        )
    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )


class CustomerView(TemplateView):
    """
    View - Для отображения заказов и их оформления на рабочую неделю
    """

    template_name = "menu/menu.html"
    top_text = "Dinners for the whole week!"
    top_text_under_text = "Everyone needs lunch or dinner"
    hello_text = "Hi {}"
    now_day = datetime.now()
    all_locations = Office.objects_active_offices.all()

    def get_context_data(self, **kwargs):
        """

        Изменяем содержание контекста. Автоматически авторизуем пользователей,
        не из числа администраторов, без пароля. Администратором буду выводить
        список пользователей по Юр лицу. Планирую отдельные учетные записи.

        :param kwargs: - словурь контеста
        :return: HTML страницу
        """
        context = super(CustomerView, self).get_context_data(**kwargs)
        context['disabled_dates'] = []
        context['all_locations'] = self.all_locations
        context['option'] = {}
        context['json_options'] = {}
        context['topText'] = self.top_text
        context['topTextUnderText'] = self.top_text_under_text
        username = context.get('username', None)
        is_group = False
        context['disabled'] = {'disabled': 'disabled'}
        context['date_list'] = list_day_from_monday_till_friday()
        if not username or username == 'None':
            context['username'] = _(
                '<i><abbr title="Most likely you are not logged in.'
                '">Anonymous</abbr> User?</i>'
            )
        else:
            user = BaseRBPIUser.objects_active_users.filter(
                username=username)
            days_which_display_on_page = [
                    context['date_list'][0][1],
                    context['date_list'][1][1],
                    context['date_list'][2][1],
                    context['date_list'][3][1],
                    context['date_list'][4][1],
                ]
            order_week = Order.objects.filter(
                order_date__in=days_which_display_on_page
            ).filter(customer=user).values(
                'first_course',
                'second_course',
                'salad',
                'order_date',
                'office__name'
            )
            disable_dates = DisableDateOrder.objects.filter(
                disabled_date__in=days_which_display_on_page
            ).values_list('disabled_date')

            for disabled_date in disable_dates:
                context['disabled_dates'].append(disabled_date[0].isoformat())

            for order in order_week:

                context['option'].update({
                    order['order_date'].isoformat(): {
                        'first': order['first_course'],
                        'second': order['second_course'],
                        'salad': order['salad'],
                        'office': json.dumps(
                            order['office__name'], cls=DjangoJSONEncoder
                        ),
                    }
                })
                context['json_options'].update({
                    order['order_date'].isoformat(): {
                        'first': order['first_course'],
                        'second': order['second_course'],
                        'salad': order['salad'],
                        'office': order['office__name'],
                    }
                })

            context['json_options'] = json.dumps(
                context['json_options'],
                cls=DjangoJSONEncoder
            )

            if not user.exists():
                context['username'] = u'{} is non existent user'.format(
                    username
                )
            else:
                context['disabled'] = {'disabled': 'enabled'}
                try:
                    user = user.get()
                except user.multipleobjectsreturned:
                    # TODO : Сделалать обработку сообщений
                    raise_message = _(
                        u'Существуют два имени: {}, ' 
                        u'напишите в службу тех., поддержки ').format(username)
                else:
                    context['is_group'] = user.is_group or is_group
                    context['user'] = username
                if not user.is_admin:
                    login(self.request, user)

        context['helloText'] = self.hello_text.format(context['username'])
        return context
