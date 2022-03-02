class Task():
    def __init__(self):
        self.id = None
        self.offload_vehicle_id=None
        self.service_vehicle_id=None
        self.allocation_basestation_id=None
        self.allocation_begin_time=None
        self.allocation_end_time=None
        self.done_status=None
        self.vehicle_density = None   #type = dic
        self.delay = None