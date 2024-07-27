import logging
from pydantic import BaseModel

from fastapi import FastAPI
from prometheus_client import multiprocess, make_asgi_app, CollectorRegistry, Gauge

app = FastAPI(title="esp32-sensor-server", version="0.0.1")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
_logger = logging.getLogger(__name__)


class SensorInfo(BaseModel):
    temp: float  # 温度
    humi: float  # 相对湿度
    co2: float  # 二氧化碳含量
    tvoc: float  # tvoc含量
    light: float  # 光强
    time_stamp: int  # 时间戳


class SensorPrometheus:
    def __init__(self):
        self.temp = Gauge("sensor_temp", "sensor temp")
        self.humi = Gauge("sensor_humi", "sensor humi")
        self.co2 = Gauge("sensor_co2", "sensor co2")
        self.tvoc = Gauge("sensor_tvoc", "sensor tvoc")
        self.light = Gauge("sensor_light", "sensor light")
        self.time_stamp = Gauge("time_stamp", "sensor get time stamp")

    def update(self, sensor_info: SensorInfo):
        self.temp.set(sensor_info.temp)
        self.humi.set(sensor_info.humi)
        self.co2.set(sensor_info.co2)
        self.tvoc.set(sensor_info.tvoc)
        self.light.set(sensor_info.light)
        self.time_stamp.set(sensor_info.time_stamp)


sensor_prometheus = SensorPrometheus()


@app.post("/sensor_info")
async def post_sensor_info(sensor_info: SensorInfo):
    _logger.info(f"sensor_info: {sensor_info}")
    sensor_prometheus.update(sensor_info)
    return {"msg": "ok"}


@app.get("/")
async def 链接测试():
    return {"status": "ok", "info": "Hello,World"}


def make_metrics_app():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return make_asgi_app(registry=registry)


metrics_app = make_metrics_app()
app.mount("/metrics", metrics_app)
