from util.BaseStation import BaseStation


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
        bs.reversed_computing_resource = row[2]
        bs.computing_efficiency = row[3]
        bs.completion_ratio = row[4]
        bs.total_received_task = row[5]
        bs.reliability = row[6]
        baseStations.append(bs)
    print(baseStations)
    return baseStations



if __name__ == '__main__':
    pass