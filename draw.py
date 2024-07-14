import datetime


def draw_graph(events,shelves_count, categories):
    index = [x.strftime('%Y-%m-%d') for x in sorted(events.keys())]
    first_date = min(events.keys())
    graph_data = {category: [0] * (len(index)+1) for category in categories}

    for category_name in graph_data:
        graph_data[category_name][-1] = shelves_count[category_name]

    first = list(sorted(events.keys()))[0]
    events[first - datetime.timedelta(days=1)] = []
    index = [(first_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')] + index


    diffs = {}
    offset = 0

    for event_date in reversed(sorted(events.keys())):

        day_events = events[event_date]
        if offset != 0:
            for category in graph_data:
                graph_data[category][-1 - offset] = graph_data[category][-1-(offset-1)] + diffs.get(category, 0)
        diffs.clear()
        for event in day_events:
            category = event['data']['category_name']
            if event['type'] == 'check':
                if category not in diffs:
                    diffs[category] = 0
                diffs[category] += event['data']['product_count']
            elif event['type'] == 'external_supply':
                if category not in diffs:
                    diffs[category] = 0
                diffs[category] -= event['data']['product_count']
        offset += 1

    return graph_data, index