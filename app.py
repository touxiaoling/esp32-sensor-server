import logging

from fastapi import FastAPI
from prometheus_client import multiprocess, make_asgi_app, CollectorRegistry, Gauge

app = FastAPI(title="esp32-sensor-server", version="0.0.2")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
_logger = logging.getLogger(__name__)


class SensorPrometheus:
    def __init__(self):
        self.promethetus_dict: dict[str, Gauge] = {}

    def update(self, sensor_info: dict[str, int | float]):
        for k, v in sensor_info.items():
            if k not in self.promethetus_dict:
                self.promethetus_dict[k] = Gauge(f"sensor_{k}", f"sensor {k}")

            self.promethetus_dict[k].set(v)


sensor_prometheus = SensorPrometheus()


@app.post("/sensor_info")
async def post_sensor_info(sensor_info: dict[str, int | float]):
    _logger.info(f"sensor_info: {sensor_info}")
    sensor_prometheus.update(sensor_info)
    return {"msg": "ok"}


@app.get("/all_sensor_info")
async def sensor_info():
    res = {k: v._value.get() for k, v in sensor_prometheus.promethetus_dict.items()}
    return res


@app.get("/")
async def 链接测试():
    return {"status": "ok", "info": "Hello,World"}


def make_metrics_app():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return make_asgi_app(registry=registry)


metrics_app = make_metrics_app()
app.mount("/metrics", metrics_app)
