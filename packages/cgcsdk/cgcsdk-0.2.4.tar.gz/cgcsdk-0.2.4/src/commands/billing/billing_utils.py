def get_status_list_to_print(costs_list: list):
    """Method format data in list of voulmes to be displayed in table and calculate total size of volumes

    :param list_of_volumes: list of volumes to be formatted
    :type list_of_volumes: list
    :return: list of volumes to be displayed in table and total size of volumes
    :rtype: list, int
    """
    list_to_print = []
    for cost in costs_list:
        rent_start = cost["rent_start"]
        rent_end = cost["rent_end"]
        rent_time = f"{int(cost['rent_time'])} s"

        total_cost = f"{float(cost['cost_total']):.2f} pln"
        resources = cost["resources"]
        name = resources["name"]
        rent_type = cost["type"]
        if rent_type == "events_compute":
            entity = resources["entity"]
        elif rent_type == "events_volume":
            entity = "volume"
        row_list = [entity, name, rent_start, rent_end, rent_time, total_cost]
        list_to_print.append(row_list)
    list_to_print.sort(key=lambda d: f"{d[0]} {d[2]}")
    return list_to_print


def get_status_list_headers():
    """Generates headers for billing status command

    :return: list of headers
    :rtype: list
    """
    headers = ["entity", "name", "start", "end", "time", "cost"]
    return headers
