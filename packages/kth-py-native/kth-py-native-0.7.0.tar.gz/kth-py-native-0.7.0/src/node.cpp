// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <kth/py-native/node.h>
#include <kth/py-native/utils.h>

#include <kth/capi.h>
#include <kth/py-native/config/settings.h>

#include <atomic>
#include <thread>

using namespace std::chrono_literals;

#ifdef __cplusplus
extern "C" {
#endif

std::atomic<bool> running_ {false};
std::atomic<bool> stopped_ {true};

PyObject* kth_py_native_node_construct(PyObject* self, PyObject* args) {
    PyObject* settings_py;
    kth_bool_t stdout_enabled_py;

    if ( ! PyArg_ParseTuple(args, "Oi", &settings_py, &stdout_enabled_py))
        return NULL;

    auto settings = kth_py_native_config_settings_to_c(settings_py);
    kth_node_t node = kth_node_construct(&settings, stdout_enabled_py);
    return PyCapsule_New(node, NULL, NULL);
}

PyObject* kth_py_native_node_destruct(PyObject* self, PyObject* args) {
    PyObject* py_node;

    // PyGILState_STATE gstate;
    // gstate = PyGILState_Ensure();

    if ( ! PyArg_ParseTuple(args, "O", &py_node))
        return NULL;

    kth_node_t node = cast_node(py_node);

    kth_node_destruct(node);
    // PyGILState_Release(gstate);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_node_init_run_sync(PyObject* self, PyObject* args) {
    PyObject* py_node;

    if ( ! PyArg_ParseTuple(args, "O", &py_node)) {
        return NULL;
    }

    kth_node_t node = cast_node(py_node);
    auto res = kth_node_init_run_sync(node, kth_start_modules_all);
    return Py_BuildValue("i", res);
}

void kth_node_run_handler(kth_node_t node, void* ctx, int error) {

    PyGILState_STATE state = PyGILState_Ensure();
    // // call python callback
    // tmp = PyObject_CallFunction((PyObject*)python_callback, "i", tid);
    // if (tmp == NULL) {
    //   PyErr_PrintEx(0);
    //   error_flag = 1; // error occured
    // }
    // Py_XDECREF(tmp);

    PyObject* py_callback = (PyObject*)ctx;

    // PyObject* arglist = Py_BuildValue("(i)", error);
    // PyObject_CallObject(py_callback, arglist);
    // Py_DECREF(arglist);


    auto tmp = PyObject_CallFunction((PyObject*)py_callback, "i", error);
    if (tmp == NULL) {
        PyErr_PrintEx(0);
        // error_flag = 1; // error occured
    }

    Py_XDECREF(py_callback);  // Dispose of the call

    PyGILState_Release(state);
}

PyObject* kth_py_native_node_init_run_and_wait_for_signal(PyObject* self, PyObject* args) {
    PyObject* py_node;
    int py_start_modules;
    PyObject* py_callback;

    if ( ! PyArg_ParseTuple(args, "OiO:set_callback", &py_node, &py_start_modules, &py_callback)) {
        return NULL;
    }

    if ( ! PyCallable_Check(py_callback)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be callable");
        return NULL;
    }

    Py_XINCREF(py_callback);         // Add a reference to new callback

    auto mods = kth_start_modules_t(py_start_modules);
    kth_node_t node = cast_node(py_node);

    std::thread t([node, py_callback, mods]() {
        kth_node_init_run_and_wait_for_signal(node, py_callback, mods, [](kth_node_t node, void* ctx, kth_error_code_t err) {
            kth_node_run_handler(node, ctx, int(err));
            running_ = true;
            stopped_ = false;
        });
        stopped_ = true;
    });
    // std::this_thread::sleep_for(2s);
    t.detach();
    Py_RETURN_NONE;
}

PyObject* kth_py_native_node_signal_stop(PyObject* self, PyObject* args) {
    PyObject* py_node;

    if ( ! PyArg_ParseTuple(args, "O", &py_node))
        return NULL;

    kth_node_t node = cast_node(py_node);

    kth_node_signal_stop(node);

    while (running_ &&  ! stopped_) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    Py_RETURN_NONE;
}

PyObject* kth_py_native_node_get_chain(PyObject* self, PyObject* args) {
    PyObject* py_node;
    if ( ! PyArg_ParseTuple(args, "O", &py_node))
        return NULL;

    kth_node_t node = cast_node(py_node);
    kth_chain_t chain = kth_node_get_chain(node);

    PyObject* py_chain = to_py_obj(chain);
    return Py_BuildValue("O", py_chain);
}

PyObject* kth_py_native_node_get_p2p(PyObject* self, PyObject* args) {
    PyObject* py_node;
    if ( ! PyArg_ParseTuple(args, "O", &py_node))
        return NULL;

    kth_node_t node = cast_node(py_node);
    kth_p2p_t p2p = kth_node_get_p2p(node);

    PyObject* py_p2p = to_py_obj(p2p);
    return Py_BuildValue("O", py_p2p);
}

PyObject* kth_py_native_node_print_thread_id(PyObject* self, PyObject* args) {
    kth_node_print_thread_id();
    Py_RETURN_NONE;
}

#ifdef __cplusplus
} // extern "C"
#endif
