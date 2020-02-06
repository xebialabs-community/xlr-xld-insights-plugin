#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
from xlrelease.HttpRequest import HttpRequest
from java.time import LocalDate, ZoneId

PAGESIZE = 25

if (server is None) or (title is None) or (timePeriod is None) or (dateAggregation is None):
    raise Exception("Values are required for mandatory tile configuration fields")

request = HttpRequest(server, username, password)

def increment_time_windows(prev_end, agg):
    if agg == "Day":
        new_start = prev_end
        new_end = prev_end.plusDays(1)
    elif agg == "Month":
        new_start = prev_end
        new_end = prev_end.plusMonths(1)
    elif agg == "Year":
        new_start = prev_end
        new_end = prev_end.plusYears(1)
    return new_start, new_end

# Get LocalDates from tile datetime properties
today = LocalDate.now()
if timePeriod == "Last 30 days":
    fromDate = today.minusDays(30)
    toDate = today
elif timePeriod == "Last 3 months":
    fromDate = today.minusMonths(3)
    toDate = today
elif timePeriod == "Last 6 months":
    fromDate = today.minusMonths(6)
    toDate = today
elif timePeriod == "Last year":
    fromDate = today.minusYears(1)
    toDate = today
else:
    fromDate = fromDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate()
    toDate = toDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate()

# Use time windows to get deployments.  This is the first window
fromRegion, toRegion = increment_time_windows(fromDate, dateAggregation)

dates = []
deployments = []
change_failure = []
period_covered = False

while fromRegion < toDate:
    deployment_count = 0
    rollback_count = 0
    results_remain = True
    page = 1
    while results_remain:
        endpoint = '/deployit/tasks/v2/query?begindate={0}&enddate={1}&page={2}&resultsPerPage={3}'.format(
            fromRegion,
            toRegion,
            page,
            PAGESIZE
        )
        response = request.get(
            endpoint,
            contentType='application/json'
        )
        if not response.isSuccessful():
            raise Exception("Failed to get deployment data from XL Deploy. Server return [%s], with content [%s]" % (response.status, response.response))
        results = json.loads(response.response)
        if results == []:
            results_remain = False
        else:
            for result in results:
                if result["metadata"]["taskType"] in ["INITIAL", "UPGRADE", "UNDEPLOY"]:
                    deployment_count += 1
                elif result["metadata"]["taskType"] == "ROLLBACK":
                    rollback_count += 1
        page += 1
    dates.append(str(fromRegion))
    deployments.append(deployment_count)
    if deployment_count > 0:
        change_failure.append(100*float(rollback_count)/float(deployment_count))
    else:
        change_failure.append(0)
    fromRegion, toRegion = increment_time_windows(toRegion, dateAggregation)

data = {
    "dates": dates,
    "deployments": deployments,
    "max_deployments": max(deployments),
    "change_failure": change_failure,
    "max_change_failure": max(change_failure),
}