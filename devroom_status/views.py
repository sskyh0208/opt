from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import DevroomStatus
import csv
import urllib
import io
import matplotlib.pyplot as plt
import os

class GraphView(ListView):
    template_name = os.path.join('devroom_status', 'graph.html')
    model = DevroomStatus
    queryset = DevroomStatus.objects.order_by('-created_at')[:60]



####################################################################################################################
# CSV出力
####################################################################################################################
def export_csv(request, type=None, year=None, month=None, day=None):
    devroom_data = DevroomStatus.objects.all().order_by('-created_at')
    filename = urllib.parse.quote(u'devroom_status.csv')
    # if type == 'year':
    #     devroom_data = DevroomStatus.objects.filter(created_at__year=year).order_by('-created_at')
    #     filename = urllib.parse.quote(u'devroom_status{}.csv').format(year).encoding('utf-8')
    # elif type == 'month':
    #     devroom_data = DevroomStatus.objects.filter(
    #         created_at__year=year,
    #         created_at__month=month
    #     ).order_by('-created_at')
    #     filename = urllib.parse.quote(u'devroom_status{}{}.csv').format(year, month).encoding('utf-8')
    # elif type == 'day':
    #     devroom_data = DevroomStatus.objects.filter(
    #         created_at__year=year,
    #         created_at__month=month,
    #         created_at__day=day
    #     ).order_by('-created_at')
    #     filename = urllib.parse.quote(u'devroom_status{}{}{}.csv').format(year, month, day).encoding('utf-8')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename*=UTF8-\'\'{filename}'
    writer = csv.writer(response)
    for data in devroom_data:
        writer.writerow([data.created_at, data.temperature, data.humidity, data.co2])
    return response
    

####################################################################################################################
# グラフ化
####################################################################################################################

def set_plt():
    # 1時間だけ
    devroom_data = DevroomStatus.objects.all().order_by('-created_at')[:60]
    # 横軸(時間)
    x = [data.created_at for data in devroom_data]
    plt.subplots(figsize=(11.0, 8.0))
    # 縦軸(気温)
    plt.subplot(3, 1, 1)
    temp = [data.temperature for data in devroom_data]
    plt.xlabel('time')
    plt.ylabel('℃')
    plt.title('temperature')
    plt.tight_layout()
    plt.plot(x, temp)

    # 縦軸(湿度)
    plt.subplot(3, 1, 2)
    humidity = [data.humidity for data in devroom_data]
    plt.xlabel('time')
    plt.ylabel('%')
    plt.title('humidity')
    plt.tight_layout()
    plt.plot(x, humidity)

    # 縦軸(二酸化炭素濃度)
    plt.subplot(3, 1, 3)
    co2 = [data.co2 for data in devroom_data]
    plt.xlabel('time')
    plt.ylabel('ppm')
    plt.title('co2')
    plt.tight_layout()
    plt.plot(x, co2)

def plt_to_svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def get_svg(request):
    set_plt()
    svg = plt_to_svg()
    plt.cla()
    return HttpResponse(svg, content_type='image/svg+xml')
