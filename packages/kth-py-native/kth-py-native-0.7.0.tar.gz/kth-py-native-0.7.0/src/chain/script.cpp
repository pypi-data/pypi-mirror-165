#include <kth/py-native/chain/script.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_script_destruct(PyObject* self, PyObject* args){
    PyObject* py_script;

    if ( ! PyArg_ParseTuple(args, "O", &py_script)) {
        return NULL;
    }

    kth_script_t script = (kth_script_t)get_ptr(py_script);
    kth_chain_script_destruct(script);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_script_is_valid(PyObject* self, PyObject* args){
    PyObject* py_script;

    if ( ! PyArg_ParseTuple(args, "O", &py_script)) {
        return NULL;
    }

    kth_script_t script = (kth_script_t)get_ptr(py_script);
    int res = kth_chain_script_is_valid(script);
    return Py_BuildValue("i", res);
}


PyObject* kth_py_native_chain_script_is_valid_operations(PyObject* self, PyObject* args){
    PyObject* py_script;

    if ( ! PyArg_ParseTuple(args, "O", &py_script)) {
        return NULL;
    }

    kth_script_t script = (kth_script_t)get_ptr(py_script);
    int res = kth_chain_script_is_valid_operations(script);
    return Py_BuildValue("i", res);
}


PyObject* kth_py_native_chain_script_satoshi_content_size(PyObject* self, PyObject* args){
    PyObject* py_script;

    if ( ! PyArg_ParseTuple(args, "O", &py_script)) {
        return NULL;
    }

    kth_script_t script = (kth_script_t)get_ptr(py_script);
    uint64_t res = kth_chain_script_satoshi_content_size(script);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_script_serialized_size(PyObject* self, PyObject* args){
    PyObject* py_script;
    int py_prefix;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_script, &py_prefix)) {
        return NULL;
    }

    kth_script_t script = (kth_script_t)get_ptr(py_script);
    uint64_t res = kth_chain_script_serialized_size(script, py_prefix);
    return Py_BuildValue("K", res);
}


PyObject* kth_py_native_chain_script_to_string(PyObject* self, PyObject* args){
    PyObject* py_script;
    uint32_t py_active_forks;

    if ( ! PyArg_ParseTuple(args, "OI", &py_script, &py_active_forks)) {
        return NULL;
    }

    kth_script_t script = (kth_script_t)get_ptr(py_script);
    char const* res = kth_chain_script_to_string(script, py_active_forks);
    return Py_BuildValue("s", res);
}

PyObject* kth_py_native_chain_script_sigops(PyObject* self, PyObject* args){
    PyObject* py_script;
    int py_embedded;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_script, &py_embedded)) {
        return NULL;
    }

    kth_script_t script = (kth_script_t)get_ptr(py_script);
    uint64_t res = kth_chain_script_sigops(script, py_embedded);
    return Py_BuildValue("K", res);
}

// PyObject* kth_py_native_chain_script_embedded_sigops(PyObject* self, PyObject* args){
//     PyObject* py_script;
//     PyObject* py_prevout_script;

//     if ( ! PyArg_ParseTuple(args, "OO", &py_script, &py_prevout_script)) {
//         return NULL;
//     }

//     kth_script_t script = (kth_script_t)get_ptr(py_script);
//     kth_script_t prevout_script = (kth_script_t)get_ptr(py_prevout_script);
//     uint64_t res = kth_chain_script_embedded_sigops(script, prevout_script);

//     KTH_EXPORT
//     kth_size_t kth_chain_script_sigops(kth_script_t script, bool_t embedded);

//     return Py_BuildValue("K", res);
// }


#ifdef __cplusplus
} // extern "C"
#endif
