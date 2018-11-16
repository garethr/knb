# KNB

A proof-of-concept CLI for getting informatiom about the status of a Knative Build object. Lets say you have a number of build jobs, you can get a list with `kubectl get build`. But how do you find more out about the job? Has it passed or failed? What was the error message if it failed? What steps comprised the build? How do you get the logs for each step? `knb` provides a simple answer.

```console
$ knb sample-124
Build       Passed    Date                 Template    Source
----------  --------  -------------------  ----------  ----------------------------------------------------
sample-124  False     2018-11-16 10:42:20  multi       https://github.com/garethr/multi-stage-build-example

build step "build-step-structure-tests" exited with code 1 (image: "docker-pullable://gcr.io/gcp-runtimes/container-
structure-test@sha256:2b7c4f4031d220bd7a72c930c563f8a66bd55abb8044480c67cbb09a078cabe2"); for logs run: kubectl -n 
default logs sample-124-zcgll -c build-step-structure-tests

Arguments (1)    Value
---------------  -------------
IMAGE            garethr/multi

Steps (6)
----------------------
credential-initializer
git-source-0
test
check
build
structure-tests
```

From the above sample we can see that the Build failed, and that the `structure-tests` step was to blame. We can then investogate further by looking at the logs for that step:

```console
$ knb sample-124 structure-tests
```

## Alternative

The above commands are really just syntactic sugar over the following:

```console
$ kubectl get build
$ kubectl get build <build-name> -o yaml
# skim the YAML document looking for the pod name
# kubectl logs <pod-name> -c build-step-<step-name>
```


## Requirements

`knb` currently uses `kubectl` rather than going directly to the Kubernetes API so `kubectl` needs to be installed and working correctly.


## Warning

*Warning* `knb` is pretty hacky and likely to explode, especially as Knative Build evolves. It's mainly a proof-of-concept to explore potential user interfaces.




