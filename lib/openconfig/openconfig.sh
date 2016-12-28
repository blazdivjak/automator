#!/usr/bin/env bash

export PYBINDPLUGIN=`/usr/bin/env python -c 'import pyangbind; import os; print "%s/plugin" % os.path.dirname(pyangbind.__file__)'`

mkdir yang     # we'll put yang models here
mkdir oc       # generated python modules will go here
# let's get openconfig models
git clone https://github.com/openconfig/public.git yang/openconfig
# we'll also need some dependencies
git clone https://github.com/YangModels/yang.git yang/extra

# generate modules for models in these folders
DIRS=(acl bgp interfaces lacp lldp local-routing policy relay-agent stp vlan)
# translate
for DIR in ${DIRS[*]}; do
    echo TRANSLATING $DIR
    pyang --plugindir $PYBINDPLUGIN -f pybind -p yang/openconfig/release/models/:yang/extra/standard/ietf/RFC/ --split-class-dir oc yang/openconfig/release/models/$DIR/*
done