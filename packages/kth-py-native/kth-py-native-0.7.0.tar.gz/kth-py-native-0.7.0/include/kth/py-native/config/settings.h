#ifndef KTH_PY_NATIVE_CONFIG_SETTINGS_H_
#define KTH_PY_NATIVE_CONFIG_SETTINGS_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/py-native/config/blockchain_settings.h>
#include <kth/py-native/config/database_settings.h>
#include <kth/py-native/config/network_settings.h>
#include <kth/py-native/config/node_settings.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    PyObject_HEAD
    PyObject* node;
    PyObject* chain;
    PyObject* database;
    PyObject* network;
} Settings;

static PyMemberDef Settings_members[] = {
    {"node", T_OBJECT_EX, offsetof(Settings, node), 0, "node"},
    {"chain", T_OBJECT_EX, offsetof(Settings, chain), 0, "chain"},
    {"database", T_OBJECT_EX, offsetof(Settings, database), 0, "database"},
    {"network", T_OBJECT_EX, offsetof(Settings, network), 0, "network"},
    {NULL}  /* Sentinel */
};

PyObject* kth_py_native_config_settings_default(PyObject* self, PyObject* args);
PyObject* kth_py_native_config_settings_get_from_file(PyObject* self, PyObject* args);

inline
kth_settings kth_py_native_config_settings_to_c(PyObject* setts) {

    PyObject* node = PyObject_GetAttrString(setts, "node");
    PyObject* chain = PyObject_GetAttrString(setts, "chain");
    PyObject* database = PyObject_GetAttrString(setts, "database");
    PyObject* network = PyObject_GetAttrString(setts, "network");

    kth_settings res;
    res.node = kth_py_native_config_node_settings_to_c(node);
    res.chain = kth_py_native_config_blockchain_settings_to_c(chain);
    res.database = kth_py_native_config_database_settings_to_c(database);
    res.network = kth_py_native_config_network_settings_to_c(network);

    return res;
}

#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_SETTINGS_H_
