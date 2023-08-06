// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/py-native/node.h>
#include <kth/py-native/utils.h>

#include <kth/capi.h>

#include <kth/capi/config/node_settings.h>

#include <kth/py-native/config/node_settings.h>
// #include <kth/py-native/helper.h>



#ifdef __cplusplus
extern "C" {
#endif

// static
// void NodeSettings_dealloc(NodeSettings* self) {
//     Py_TYPE(self)->tp_free((PyObject*) self);
// }

// static
// PyObject* NodeSettings_new(PyTypeObject *type, PyObject* args, PyObject* kwds) {
//     NodeSettings* self;
//     self = (NodeSettings*) type->tp_alloc(type, 0);
//     if (self != NULL) {
//         self->sync_peers = 0;
//         self->sync_timeout_seconds = 0;
//         self->block_latency_seconds = 0;
//         self->refresh_transactions = 0;
//         self->compact_blocks_high_bandwidth = 0;
//         self->ds_proofs_enabled = 0;
//     }
//     return (PyObject* ) self;
// }

// static
// int NodeSettings_init(NodeSettings* self, PyObject* args, PyObject* kwds) {
//     static char* kwlist[] = {
//         "sync_peers",
//         "sync_timeout_seconds",
//         "block_latency_seconds",
//         "refresh_transactions",
//         "compact_blocks_high_bandwidth",
//         "ds_proofs_enabled",
//         NULL};

//     if ( ! PyArg_ParseTupleAndKeywords(args, kwds, "|iiiiii", kwlist,
//                                      &self->sync_peers,
//                                      &self->sync_timeout_seconds,
//                                      &self->block_latency_seconds,
//                                      &self->refresh_transactions,
//                                      &self->compact_blocks_high_bandwidth,
//                                      &self->ds_proofs_enabled
//                                      )) {
//         return -1;
//     }


//     return 0;
// }

// static
// PyObject* NodeSettings_name(NodeSettings* self, PyObject* Py_UNUSED(ignored)) {
//     if (self->first == NULL) {
//         PyErr_SetString(PyExc_AttributeError, "first");
//         return NULL;
//     }
//     if (self->last == NULL) {
//         PyErr_SetString(PyExc_AttributeError, "last");
//         return NULL;
//     }
//     return PyUnicode_FromFormat("%S %S", self->first, self->last);
// }

// static PyMethodDef NodeSettings_methods[] = {
//     // {"name", (PyCFunction) NodeSettings_name, METH_NOARGS, "Return the name, combining the first and last name"},
//     {NULL}  /* Sentinel */
// };

// static PyTypeObject NodeSettingsType = {
//     PyVarObject_HEAD_INIT(NULL, 0)
//     .tp_name = "custom2.NodeSettings",
//     .tp_doc = "Node Settings",
//     .tp_basicsize = sizeof(NodeSettings),
//     .tp_itemsize = 0,
//     .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
//     .tp_new = NodeSettings_new,
//     .tp_init = (initproc) NodeSettings_init,
//     .tp_dealloc = (destructor) NodeSettings_dealloc,
//     .tp_members = NodeSettings_members,
//     .tp_methods = NodeSettings_methods,
// };


// PyMODINIT_FUNC
// PyInit_custom2(void) {
//     PyObject* m;
//     if (PyType_Ready(&CustomType) < 0)
//         return NULL;

//     m = PyModule_Create(&custommodule);
//     if (m == NULL)
//         return NULL;

//     Py_INCREF(&CustomType);
//     if (PyModule_AddObject(m, "NodeSettings", (PyObject* ) &CustomType) < 0) {
//         Py_DECREF(&CustomType);
//         Py_DECREF(m);
//         return NULL;
//     }

//     return m;
// }



// void config_node_settings_default(v8::FunctionCallbackInfo<v8::Value> const& args) {
//     Isolate* isolate = args.GetIsolate();

//     if (args.Length() != 1) {
//         throw_exception(isolate, "Wrong number of arguments. config_node_settings_default function requires 1 arguments.");
//         return;
//     }

//     if ( ! args[0]->IsNumber()) {
//         throw_exception(isolate, "Wrong argument type for argument network (#1). Required to be IsNumber.");
//         return;
//     }

//     kth_network_t network = network_to_cpp(isolate, args[0]);
//     kth_node_settings res = kth_config_node_settings_default(network);
//     args.GetReturnValue().Set(detail::config_node_settings_to_js(isolate, res));
// }



#ifdef __cplusplus
} // extern "C"
#endif
