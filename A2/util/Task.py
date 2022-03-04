class Task():
    def __init__(self,id=None,o_id=None,s_id=None,a_id=None,status=None,density=None,delay=None):
        self.id = id
        self.offload_vehicle_id=o_id
        self.service_vehicle_id=s_id
        self.allocation_basestation_id=a_id
        self.done_status=status
        self.vehicle_density = density   #type = dic
        self.delay = delay