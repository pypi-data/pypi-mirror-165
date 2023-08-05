import datetime
import json
import os
import subprocess
import traceback

import coolname

from deque.rest_connect import RestConnect
from deque.deque_environment import AGENT_API_SERVICE_URL
from deque.redis_services import RedisServices
import pickle
import multiprocessing
from deque.parsing_service import ParsingService
from deque.datatypes import Image, Audio, Histogram, BoundingBox2D, Table, Plot
from deque.util import MODEL, CODE, DATA, ENVIRONMENT, RESOURCES,TRACKING_ENDPOINT
import requests
import glob
import time
import psutil
import GPUtil
import socket

'''
def decode_datetime(obj):
    if '__datetime__' in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    return obj


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj
'''


def _start_transport_service():
    try:
        print("Starting transport")
        import redis_server
        bin_path = str(redis_server.REDIS_SERVER_PATH)
        subprocess.run([bin_path])
        print("started successfully")
    except Exception as e:
        print(e)
        traceback.print_exc()


#_start_transport_service()

_RESOURCE_MONITORING_INTERVAL = 60


class Run:

    # _submission_count = 1
    def __init__(self):
        self.user_name = None

        self._workload_type = None
        # self._submission_id = None

        self.project_id = None
        self._project_name = None
        self._workload_id = None
        self._api_key = None
        self._submission_id = None
        self._agent_id = None
        self.params = dict()
        self._history = dict()
        self._step = 1
        self._run_id = None
        self._rest = RestConnect()
        self._redis = RedisServices.get_redis_connection()
        self._agent_network_details = self._get_network_details()
        self._run_meta_data = None
        self._model_logged = False

        self._code_logged = False
        self._running = False
        self._environment_logged = False

        self._resources_logged = False
        self._res_monitor = None

    def init(self, user_name, project_name=None, api_key=None):
        os.environ["running"] = "yes"
        self._running = True
        self.user_name = user_name

        self._api_key = api_key

        is_authenticated = self._authenticate()
        if not is_authenticated:
            raise ValueError("Invalid user and/or api key")

        self._workload_type = os.getenv("workload_type")
        self._workload_id = os.getenv("workload_id")
        self._submission_id = os.getenv("submission_id")
        self._agent_id = os.getenv("agent_id")

        if project_name is None:
            if self._workload_id is None:
                raise ValueError("Project name cannot be empty")
            else:
                self._project_name = self._workload_id
        else:
            self._project_name = project_name
        self._run_id = str(coolname.generate_slug(2))
        self._step = 1

        p2 = multiprocessing.Process(target=self._start_parser)
        p2.start()

        self._res_monitor = multiprocessing.Process(target=self._monitor_resources, args=(
        self._agent_id, self._run_id, self.user_name, self._project_name, self._workload_id,
        self._submission_id, self._workload_type))
        self._res_monitor.start()
        self._redis.flushall()
        self._redis.sadd("run_ids:", self._run_id)

        self._run_meta_data = {"submission_id": self._submission_id, "run_id": self._run_id,
                               "workload_type": self._workload_type, "workload_id": self._workload_id,
                               "project_name": self._project_name, "user_name": user_name}

        self._model_logged = False

        self._code_logged = False

        self._environment_logged = False

        self._resources_logged = False

        print(f"Run initialized with project name as {self._project_name} and run id {self._run_id}")

    def _start_parser(self):
        parser = ParsingService()
        parser.receive()

    def finish(self):
        self._running = False
        os.environ["running"]="no"
        if self._res_monitor is not None:
            self._res_monitor.terminate()

    def _monitor_resources(self, agent_id, run_id, user_name, project_name, workload_id, submission_id,
                           workload_type):
        running = os.getenv("running")
        step=os.getenv("step")
        while running=="yes":
            running = os.getenv("running")
            gpu_count = len(GPUtil.getGPUs())
            gpu_list = []

            for i in range(gpu_count):
                gpu_dict = {}
                gpu_dict['gpu_name'] = GPUtil.getGPUs()[i].name
                gpu_dict['gpu_driver'] = GPUtil.getGPUs()[i].driver
                gpu_dict['total_memory'] = GPUtil.getGPUs(
                )[i].memoryTotal / 1024  # converted to GB
                gpu_dict['gpu_free_memory'] = GPUtil.getGPUs()[i].memoryFree
                gpu_dict['current_gpu_load'] = 100 * GPUtil.getGPUs()[i].load
                gpu_list.append(gpu_dict)

            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)

            monitoring_info = {
                'agent_id': agent_id,
                'run_id': run_id,
                'user_name': user_name,
                'project_name': project_name,
                'step': step,
                'workload_id': workload_id,
                'submission_id': submission_id,
                'workload_type': workload_type,
                'current_cpu_usage': float(psutil.cpu_percent(interval=1)),
                'cpu_count': int(psutil.cpu_count()),
                'cpu_cores': int(psutil.cpu_count(logical=True)),
                # /(1024*1024*1024) ,# converted to GB
                'available_memory': int(psutil.virtual_memory()[1]),
                # / (1024*1024*1024) ,# converted to GB
                'total_memory': psutil.virtual_memory()[0],
                'memory_utilization': psutil.virtual_memory()[2],

                'current_network_usage': 'unknown',
                'current_gpu_usage': gpu_list,
                'free_disk_space': psutil.disk_usage(os.path.sep)[1],

                'ip_address': host_ip,
                'gpu_list': gpu_list,
                'gpu_count': len(gpu_list),

                'agent_network_details': self._agent_network_details,

            }

            # monitoring_info.update({"dq_instance_type":self.dq_instance_type})

            # self.dq_instance_type = dq_instance_type

            try:
                resp = self._rest.post(
                    AGENT_API_SERVICE_URL + '/fex/experiment/monitor/',
                    json=monitoring_info, )

            except requests.exceptions.ConnectionError as e:
                traceback.print_exc(e)
                time.sleep(10)
                self._monitor_resources(agent_id, run_id, user_name, project_name, workload_id, submission_id,
                           workload_type)
            except Exception as ge:
                traceback.print_exc(ge)
                time.sleep(10)
                self._monitor_resources(agent_id, run_id, user_name, project_name, workload_id, submission_id,
                           workload_type)

            time.sleep(_RESOURCE_MONITORING_INTERVAL)

    def _get_network_details(self):

        interfaces = psutil.net_if_addrs()
        hostname = socket.gethostname()
        fqdn = socket.getfqdn()

        agent_network_details = {'hostname': hostname, 'fqdn': fqdn}

        agent_ip_details = []

        for name, addrs in interfaces.items():
            # print(name, addrs)

            status = {
                "ipv4": "-",
                "ipv6": "-",
                "mac": "-"
            }

            for addr in addrs:
                if addr.family == socket.AF_INET and addr.netmask is not None:
                    status["ipv4"] = addr.address

                    agent_ip_detail = {'name': name, 'ip_address': addr.address, 'netmask': addr.netmask}
                    agent_ip_details.append(agent_ip_detail)

                if addr.family == socket.AF_INET6:
                    status["ipv6"] = addr.address

                if addr.family == psutil.AF_LINK:
                    status["mac"] = addr.address

        agent_network_details.update({'agent_ip_details': agent_ip_details})

        return agent_network_details

    def _send_data_to_redis(self, step, data):

        key = "run_id:step:data:" + self._run_id + str(step)

        self._redis.sadd("run_id:steps:" + self._run_id, str(step))

        data_pickled = pickle.dumps(data)

        self._redis.set(key, data_pickled)

    def log(self, data, step=None, commit=True):
        self._validate_data(data=data)
        full_data = {"experiment_data": data}
        full_data.update(
            {"user_name": self.user_name, "run_id": self._run_id, "workload_type": self._workload_type,
             "workload_id": self._workload_id, "submission_id": self._submission_id,
             "project_name": self._project_name, "deque_log_time": datetime.datetime.now(), "step": self._step})
        p = multiprocessing.Process(target=self._log_task, args=(full_data, self._run_meta_data))
        p.start()
        #self._send_data_to_redis(step=self._step, data=full_data)
        os.environ['step']=str(self._step)
        if commit:
            self._step += 1

    def _log_task(self, data, run_meta_data):
        pickled_data = pickle.dumps(data)
        self._rest.post_binary(url=TRACKING_ENDPOINT, data=pickled_data)

    def log_artifact(self, artifact_type, path):
        if self._run_meta_data is None:
            raise ValueError("Run not initialized. Please call init first")
        # s3://dequeapp-deque/users/riju@deque.app/projects/dex_audio/runs/adamant-galago/
        if artifact_type == MODEL:
            self._model_logged = True
        elif artifact_type == CODE:
            self._code_logged = True
        elif artifact_type == ENVIRONMENT:
            self._environment_logged = True
        elif artifact_type == RESOURCES:
            self._resources_logged = True
        p2 = multiprocessing.Process(target=self._log_artifact_task, args=(artifact_type, path, self._run_meta_data))
        p2.start()

    def _log_artifact_task(self, artifact_type, path, run_meta_data):

        print("I am saving artifact")
        file_name = os.path.basename(path)

        if artifact_type == MODEL:
            dest_path = "users/" + self.user_name + "/projects/" + self._project_name + "/runs/" + self._run_id + "/model/" + file_name
        elif artifact_type == CODE:
            dest_path = "users/" + self.user_name + "/projects/" + self._project_name + "/runs/" + self._run_id + "/code/"
        elif artifact_type == ENVIRONMENT:
            dest_path = "users/" + self.user_name + "/projects/" + self._project_name + "/runs/" + self._run_id + "/environment/" + file_name




        elif artifact_type == RESOURCES:
            dest_path = "users/" + self.user_name + "/projects/" + self._project_name + "/runs/" + self._run_id + "/resources/"
        else:
            raise ValueError(
                "artifact_type must be model (file), environment (file), code (file) or resources (directory)")

        print(AGENT_API_SERVICE_URL + "/fex/drive/contents/upload/presigned_url/read/")

        # Demonstrate how another Python program can use the presigned URL to upload a file
        if os.path.isdir(path):
            artifact_uris = []
            for filename in glob.iglob(path + '**/**', recursive=True):
                if os.path.isdir(filename):
                    continue
                dest_path = dest_path + filename
                req_data = {"user_name": self.user_name, "destination_path": dest_path}
                resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/drive/contents/upload/presigned_url/read/",
                                     json=req_data)
                res = resp.json()
                print(res)
                with open(filename, 'rb') as f:
                    files = {'file': (filename, f)}
                    if "fields" in res:
                        http_response = requests.post(url=res['url'], data=res['fields'], files=files)
                    else:
                        # TODO: for google we need a different way to save data
                        object_text = f.read()
                        headers = {'Content-type': "application/octet-stream"}
                        http_response = requests.put(url=res['url'], data=object_text, headers=headers)
                    print(http_response)
                # we record the meta data
            artifact_uris.append(dest_path)
            req_data = {"user_name": self.user_name, "destination_path": dest_path, "artifact_type": artifact_type,
                        "project_name": self._project_name, "run_id": self._run_id, "artifact_uris": artifact_uris}
            resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/artifact/metadata/create/",
                                 json=req_data)
            res = resp.json()
            print(res)

        else:
            req_data = {"user_name": self.user_name, "destination_path": dest_path}
            resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/drive/contents/upload/presigned_url/read/",
                                 json=req_data)
            res = resp.json()
            with open(path, 'rb') as f:
                files = {'file': (path, f)}
                if "fields" in res:
                    http_response = requests.post(url=res['url'], data=res['fields'], files=files)
                else:
                    # TODO: for google we need a different way to save data
                    object_text = f.read()
                    headers = {'Content-type': "application/octet-stream"}
                    http_response = requests.put(url=res['url'], data=object_text, headers=headers)
                print(http_response)
            req_data = {"user_name": self.user_name, "destination_path": dest_path, "artifact_type": artifact_type,
                        "project_name": self._project_name, "run_id": self._run_id, "artifact_uris": [dest_path]}
            resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/artifact/metadata/create/",
                                 json=req_data)
            res = resp.json()
            print(res)

        # If successful, returns HTTP status code 204

    def register_artifacts(self, latest=True, label=None, tags=None):
        if not self._model_logged:
            raise ValueError(
                "Please log the model (and optionally code and environment) before calling register_artifacts")
        req_data = {"user_name": self.user_name, "latest": latest, "label": label,
                    "project_name": self._project_name, "run_id": self._run_id, "tags": tags}
        resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/project/artifacts/register/",
                             json=req_data)
        res = resp.json()
        print(res)




    def load_model(self, model, version="latest"):
        self.user_name = "riju@deque.app"
        self._project_name = "dex_audio"
        self._run_id = "adamant-galago"
        print("I am loading model artifact")

    def _validate_data(self, data):
        for key, value in data.items():
            if type(value) is dict:
                self._validate_data(value)
            else:
                # print(type(value))
                if type(value) in [Audio, BoundingBox2D, Histogram,Table,
                                   Image, Plot] or value.__class__.__module__ == '__builtin__':
                    pass
                else:
                    raise ValueError(
                        "Invalid type in dictionary. Allowed values include builtin types and Deque data types " + str(
                            type(value)) + " " + str(value.__class__.__module__))

    def _send_upstream(self):
        self._rest.post(url=AGENT_API_SERVICE_URL + "/fex/python/track/", json=self._history)
        self._history = dict()

    def _authenticate(self):
        return True


if __name__ == "__main__":
    deque = Run()

    deque.log_artifact_task(artifact_type=RESOURCES, path="/home/riju/Documents/deque/dequeapp/dequeapp.egg-info",
                            run_meta_data=None)
    # deque.init(user_name="riju@deque.app", project_name="awesome-dude")
    # for i in range(100):
    # deque.log(data={"train": {"accuracy": i, "loss": i - 100}, "image": deque.im})

    # deque.log(data={"image":deque.im})
