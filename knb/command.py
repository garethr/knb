#!/usr/bin/env python

import subprocess
import pprint

import click
from tabulate import tabulate
import yaml


def summary(data):
    name = data["metadata"]["name"]
    template_name = data["spec"]["template"]["name"]
    source = data["spec"]["source"]["git"]["url"]

    arguments = []
    for arg in data["spec"]["template"]["arguments"]:
        arguments.append([arg["name"], arg["value"]])

    status = data["status"]["conditions"][0]["status"]
    status_date = data["status"]["conditions"][0]["lastTransitionTime"]

    if status == "True":
        fg = "green"
    else:
        fg = "red"

    status_styled = click.style(status, fg=fg)

    steps = []
    for step in data["status"]["stepsCompleted"]:
        steps.append([step.replace("build-step-", "", 1)])

    table = []
    table.append([name, status_styled, status_date, template_name, source])


    click.echo(tabulate(table, headers=["Build", "Passed", "Date", "Template", "Source"]))
    click.echo()
    if status == "False":
        message = data["status"]["conditions"][0]["message"]
        click.echo(message)
        click.echo()
    click.echo(tabulate(arguments, headers=["Arguments ({})".format(len(arguments)), "Value"]))
    click.echo()
    click.echo(tabulate(steps, headers=["Steps ({})".format(len(steps))]))


def logs(data, step):
    pod_name = data["status"]["cluster"]["podName"]
    command = subprocess.Popen(
        "kubectl.exe logs {name} -c build-step-{step}".format(name=pod_name, step=step), shell=True, stdout=subprocess.PIPE
    )
    while command.poll() is None:
        output = command.stdout.readline().rstrip()
        if output:
            click.echo(output)


@click.command()
@click.argument("name")
@click.argument("step", required=False)
def cli(name, step):
    """
    Display details of a Knative Build.
    Passing a second argument will show the logs for that particular step.

    """
    command = subprocess.run(
        "kubectl.exe get build {} -o yaml".format(name), capture_output=True, shell=True
    )
    if command.returncode == 0:
        doc = command.stdout.decode()
        data = yaml.load(doc)
    else:
        exit(command.stderr.decode())
    if step:
        logs(data, step)
    else:
        summary(data)


if __name__ == "__main__":
    cli()
