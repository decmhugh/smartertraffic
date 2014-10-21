from django.http import StreamingHttpResponse
import smartcity.module.JunctionData as jd
import smartcity.module.modelling.AnalyseTrafficData as atd
import smartcity.module.twitter.TwitterServiceAA as aa
import smartcity.module.WebTrafficData as wtd
import smartcity.module.twitter.TwitterService as ts
import smartcity.module.modelling.arima.WeatherDataOutput as wecorr
import smartcity.module.preprocessing.AnalyseTrafficDistributionData as dist
import smartcity.module.modelling.prediction.TrafficResults as tr
from json import dumps, loads, JSONEncoder

def hello_world(request):
    return StreamingHttpResponse("Hello world")

def traffic(request):
    data = jd.json_str({"direction":request.GET.get("direction")});
    print(data)
    return StreamingHttpResponse(data)

def analyse(request):
    return StreamingHttpResponse(wtd.data(request.GET.get("id")))


def trafficresult(request):
    resultManager = tr.TrafficResults()
    return StreamingHttpResponse(resultManager.highestall())

def twitter(request):
    date = {"_id":request.GET.get("date")}
    return StreamingHttpResponse(ts.feed(date))

def twitterresult(request):
    date = request.GET.get("date")
    print(date)
    return StreamingHttpResponse(dumps(ts.predict(date)))

def distribution(request):
    return StreamingHttpResponse(dumps(dist.dist()))

def distribution_weekday(request):
    return StreamingHttpResponse(dumps(dist.weekday()))

def distribution_weekend(request):
    return StreamingHttpResponse(dumps(dist.weekend()))

def tweetcloud_aa(request):
    return StreamingHttpResponse(dumps(aa.feed("")))

def weather_corr(request):
    return StreamingHttpResponse(wecorr.weather_corr().to_json())