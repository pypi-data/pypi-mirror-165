#ifndef KTH_PY_NATIVE_CONFIG_NODE_SETTINGS_H_
#define KTH_PY_NATIVE_CONFIG_NODE_SETTINGS_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/py-native/config/common.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    PyObject_HEAD
    uint32_t sync_peers;
    uint32_t sync_timeout_seconds;
    uint32_t block_latency_seconds;
    kth_bool_t refresh_transactions;
    kth_bool_t compact_blocks_high_bandwidth;
    kth_bool_t ds_proofs_enabled;
} NodeSettings;

static PyMemberDef NodeSettings_members[] = {
    {"sync_peers", T_INT, offsetof(NodeSettings, sync_peers), 0, "sync_peers"},
    {"sync_timeout_seconds", T_INT, offsetof(NodeSettings, sync_timeout_seconds), 0, "sync_timeout_seconds"},
    {"block_latency_seconds", T_INT, offsetof(NodeSettings, block_latency_seconds), 0, "block_latency_seconds"},
    {"refresh_transactions", T_INT, offsetof(NodeSettings, refresh_transactions), 0, "refresh_transactions"},
    {"compact_blocks_high_bandwidth", T_INT, offsetof(NodeSettings, compact_blocks_high_bandwidth), 0, "compact_blocks_high_bandwidth"},
    {"ds_proofs_enabled", T_INT, offsetof(NodeSettings, ds_proofs_enabled), 0, "ds_proofs_enabled"},
    {NULL}  /* Sentinel */
};

PyObject* kth_py_native_config_node_settings_default(PyObject* self, PyObject* args);

inline
kth_node_settings kth_py_native_config_node_settings_to_c(PyObject* setts) {
    kth_node_settings res;
    KTH_PY_GETATTR(res, setts, sync_peers, "i");
    KTH_PY_GETATTR(res, setts, sync_timeout_seconds, "i");
    KTH_PY_GETATTR(res, setts, block_latency_seconds, "i");
    KTH_PY_GETATTR(res, setts, refresh_transactions, "i");
    KTH_PY_GETATTR(res, setts, compact_blocks_high_bandwidth, "i");
    KTH_PY_GETATTR(res, setts, ds_proofs_enabled, "i");
    return res;

    // PyObject* sync_peers = PyObject_GetAttrString(setts, "sync_peers");
    // PyObject* sync_timeout_seconds = PyObject_GetAttrString(setts, "sync_timeout_seconds");
    // PyObject* block_latency_seconds = PyObject_GetAttrString(setts, "block_latency_seconds");
    // PyObject* refresh_transactions = PyObject_GetAttrString(setts, "refresh_transactions");
    // PyObject* compact_blocks_high_bandwidth = PyObject_GetAttrString(setts, "compact_blocks_high_bandwidth");
    // PyObject* ds_proofs_enabled = PyObject_GetAttrString(setts, "ds_proofs_enabled");

    // kth_node_settings res;

    // if ( ! PyArg_ParseTuple(sync_peers, "i", &res.sync_peers))
    //     return res;

    // if ( ! PyArg_ParseTuple(sync_timeout_seconds, "i", &res.sync_timeout_seconds))
    //     return res;

    // if ( ! PyArg_ParseTuple(block_latency_seconds, "i", &res.block_latency_seconds))
    //     return res;

    // if ( ! PyArg_ParseTuple(refresh_transactions, "i", &res.refresh_transactions))
    //     return res;

    // if ( ! PyArg_ParseTuple(compact_blocks_high_bandwidth, "i", &res.compact_blocks_high_bandwidth))
    //     return res;

    // if ( ! PyArg_ParseTuple(ds_proofs_enabled, "i", &res.ds_proofs_enabled))
    //     return res;

    // return res;
}

// PyObject* kth_py_native_config_node_settings_to_py(kth_node_settings const& setts) {
//     PyObject* obj = PyObject_CallFunction((PyObject*)&NodeSettingsType, NULL);

//     auto res2 = KTH_PY_SETATTR(obj, setts, sync_peers, "i");
//          res2 = KTH_PY_SETATTR(obj, setts, sync_timeout_seconds, "i");
//          res2 = KTH_PY_SETATTR(obj, setts, block_latency_seconds, "i");
//          res2 = KTH_PY_SETATTR(obj, setts, refresh_transactions, "i");
//          res2 = KTH_PY_SETATTR(obj, setts, compact_blocks_high_bandwidth, "i");
//          res2 = KTH_PY_SETATTR(obj, setts, ds_proofs_enabled, "i");

//     return obj;
// }


#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_NODE_SETTINGS_H_
