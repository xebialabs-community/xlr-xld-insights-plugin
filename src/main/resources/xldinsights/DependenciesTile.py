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

def get_applications(ancestor, applications_count):
    request = HttpRequest(server, username, password)
    applications_batch = []
    results_remain = True
    page = 0
    while results_remain:
        endpoint = '/deployit/repository/query?page={}&resultsPerPage=100&type=udm.Application&ancestor={}'.format(
            page,
            ancestor
        )
        response = request.get(
            endpoint,
            contentType='application/json'
        )
        if not response.isSuccessful():
            raise Exception("Failed to get application information from XL Deploy. Server return [%s], with content [%s]" % (response.status, response.response))
        results = json.loads(response.response)
        if results == []:
            results_remain = False
        else:
            for result in results:
                applications_batch.append(
                    {
                        "id": "{}".format(applications_count),
                        "name": result["ref"]
                    }
                )
                applications_count += 1
            page += 1
    return {"batch": applications_batch, "count": applications_count}

def get_applications_metadata(applications):
    request = HttpRequest(server, username, password)
    application_metadata = {}
    for application in applications:
        applicationShortName = application["name"].split('/')[-1]
        application_metadata[applicationShortName] = {}

        application_metadata[applicationShortName]["plotId"] = application["id"]
        
        endpoint = '/deployit/repository/ci/{}'.format(application["name"])
        response = request.get(
            endpoint,
            contentType='application/json'
        )
        if not response.isSuccessful():
            raise Exception("Failed to get application information from XL Deploy. Server return [%s], with content [%s]" % (response.status, response.response))
        lastVersion = json.loads(response.response)["lastVersion"]
        application_metadata[applicationShortName]["lastVersion"] = lastVersion

        if lastVersion == "":
            applicationDependencies = []
        else:
            endpoint = '/deployit/repository/ci/{}/{}'.format(application["name"], lastVersion)
            response = request.get(
                endpoint,
                contentType='application/json'
            )
            if not response.isSuccessful():
                raise Exception("Failed to get deployment package information from XL Deploy. Server return [%s], with content [%s]" % (response.status, response.response))
            if json.loads(response.response)["type"] == "udm.CompositePackage":
                applicationDependencies = []
            else:
                applicationDependencies = json.loads(response.response)["applicationDependencies"].keys()
        application_metadata[applicationShortName]["applicationDependencies"] = applicationDependencies

        application_metadata[applicationShortName]["dependedUponCount"] = 0

    for application in application_metadata.keys():
        for dependency in application_metadata[application]["applicationDependencies"]:
            if dependency in application_metadata.keys():  # only add if dependency exists in XLD
                application_metadata[dependency]["dependedUponCount"] += 1

    return application_metadata

def compile_plot_components(applications, application_metadata):
    links = []
    for application in application_metadata.keys():
        for dependency in application_metadata[application]["applicationDependencies"]:
            if dependency in application_metadata.keys():  # only add if dependency exists in XLD
                link_id = len(links)
                links.append(
                    {
                        "id": "{}".format(link_id),
                        "source": "{}".format(application_metadata[application]["plotId"]),
                        "target": "{}".format(application_metadata[dependency]["plotId"]),
                        "lineStyle": {
                            "normal": {}
                        }
                    }
                )

    categories = []
    for i in range(len(applications)):
        applicationParentFolder = applications[i]["name"].split('/')[-2]
        if applicationParentFolder not in categories:
            categories.append(applicationParentFolder)

    nodes = []
    for i in range(len(applications)):
        applicationShortName = applications[i]["name"].split('/')[-1]
        applicationParentFolder = applications[i]["name"].split('/')[-2]
        nodes.append(
            {
                "id": applications[i]["id"],
                "name": applicationShortName,
                "symbolSize": 20+2*len(application_metadata[applicationShortName]["applicationDependencies"]),
                "value": 20+2*len(application_metadata[applicationShortName]["applicationDependencies"]),
                "category": categories.index(applicationParentFolder),
                "lastVersion": application_metadata[applicationShortName]["lastVersion"],
                "dependenciesCount": len(application_metadata[applicationShortName]["applicationDependencies"]),
                "dependedUponCount": application_metadata[applicationShortName]["dependedUponCount"],
                "label": {
                    "normal": {
                        "show": True
                    }
                }
            }
        )

    # Some echarts formatting and rewriting key names for better presentation
    categories = [{"name": category} for category in categories]
    for i in range(len(categories)):
        if categories[i]["name"] == "Applications":
            categories[i]["name"] = "Root Folder"
            break
    for i in range(len(nodes)):
        if nodes[i]["category"] == "Applications":
            nodes[i]["category"] = "Root Folder"
    for i in range(len(nodes)):
        if nodes[i]["lastVersion"] == "":
            nodes[i]["lastVersion"] = "-"

    return {"nodes": nodes, "links": links, "categories": categories}

if folders is None:
    ancestors = ["Applications"]
else:
    ancestors = list(folders)[:]
applications = []
applications_count = 0
for ancestor in ancestors:
    ancestor_applications = get_applications(ancestor, applications_count)
    applications += ancestor_applications["batch"]
    applications_count = ancestor_applications["count"]

application_metadata = get_applications_metadata(applications)

plot_components = compile_plot_components(applications, application_metadata)

data = {
    "nodes": plot_components["nodes"],
    "links": plot_components["links"],
    "categories": plot_components["categories"]
}