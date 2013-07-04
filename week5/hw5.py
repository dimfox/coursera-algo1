import dijstra


def solve(file_name):
    graph = dijstra.read_input(file_name)
    dist = dijstra.dijstra(graph, 1)
    result = [0] * len(dist)
    for n in dist:
        result[n-1] = dist[n]

    return result


def testcases():
    test1 = solve('test1.txt')
    assert test1 == [0,10,50,30,60]

    test2 = solve('test2.txt')
    assert test2 == [0, 45,10,25,45,float('inf')]

if __name__ == '__main__':
    #testcases()
    import datetime
    start_time = datetime.datetime.now()
    print start_time, 'start solving'
    for _ in range(100):
        dist = solve('dijkstraData.txt')
    end_time = datetime.datetime.now()
    print end_time, 'end solving'
    print end_time - start_time
    report_result = []
    for node in [7,37,59,82,99,115,133,165,188,197]:
        report_result.append(str(dist[node-1]))
    print ','.join(report_result)
