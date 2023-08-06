#ifndef KTH_PY_NATIVE_CONFIG_DATABASE_SETTINGS_H_
#define KTH_PY_NATIVE_CONFIG_DATABASE_SETTINGS_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/py-native/config/common.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    PyObject_HEAD
    PyObject* directory;
    kth_bool_t flush_writes;
    uint16_t file_growth_rate;
    uint32_t index_start_height;
    uint32_t reorg_pool_limit;
    uint64_t db_max_size;
    kth_bool_t safe_mode;
    uint32_t cache_capacity;
} DatabaseSettings;

static PyMemberDef DatabaseSettings_members[] = {
    {"directory", T_OBJECT_EX, offsetof(DatabaseSettings, directory), 0, "directory"},
    {"flush_writes", T_INT, offsetof(DatabaseSettings, flush_writes), 0, "flush_writes"},
    {"file_growth_rate", T_UINT, offsetof(DatabaseSettings, file_growth_rate), 0, "file_growth_rate"},
    {"index_start_height", T_UINT, offsetof(DatabaseSettings, index_start_height), 0, "index_start_height"},
    {"reorg_pool_limit", T_UINT, offsetof(DatabaseSettings, reorg_pool_limit), 0, "reorg_pool_limit"},
    {"db_max_size", T_ULONGLONG, offsetof(DatabaseSettings, db_max_size), 0, "db_max_size"},
    {"safe_mode", T_INT, offsetof(DatabaseSettings, safe_mode), 0, "safe_mode"},
    {"cache_capacity", T_UINT, offsetof(DatabaseSettings, cache_capacity), 0, "cache_capacity"},
    {NULL}  /* Sentinel */
};

PyObject* kth_py_native_config_database_settings_default(PyObject* self, PyObject* args);

inline
kth_database_settings kth_py_native_config_database_settings_to_c(PyObject* setts) {
    kth_database_settings res;

    KTH_PY_GETATTR(res, setts, directory, "s");
    KTH_PY_GETATTR(res, setts, flush_writes, "i");
    KTH_PY_GETATTR(res, setts, file_growth_rate, "I");
    KTH_PY_GETATTR(res, setts, index_start_height, "I");
    KTH_PY_GETATTR(res, setts, reorg_pool_limit, "I");
    KTH_PY_GETATTR(res, setts, db_max_size, "K");
    KTH_PY_GETATTR(res, setts, safe_mode, "i");
    KTH_PY_GETATTR(res, setts, cache_capacity, "I");

    return res;
}

#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_DATABASE_SETTINGS_H_
