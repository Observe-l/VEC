from util.BaseStation import *


def BSDF2BS(baseStationDF):
    """transfer dataframe into basestation
    input: dataframe type
    output:basestation list type
    """
    baseStationvalues = baseStationDF.values
    baseStations = []
    for row in baseStationvalues:
        bs = BaseStation()
        bs.id = row[0]
        bs.global_computing_resource = row[1]
        bs.reserved_computing_resource = row[2]
        bs.vehicle_density = row[3]
        bs.computing_efficiency = row[4]
        bs.completion_ratio = row[5]
        bs.total_received_task = row[6]
        bs.reliability = row[7]
        baseStations.append(bs)
    print(baseStations)
    return baseStations



if __name__ == '__main__':
    pass