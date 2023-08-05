#include <Python.h>
#include "../../qinfo/src/unix.h"
#include "../../qinfo/src/config.h"

typedef PyObject pyob;

static pyob *qinfo_get_core_count(pyob *self)
{
  int sts;
  sts = get_core_count();
  return Py_BuildValue("i", sts);
}

static pyob *version(pyob *self)
{
  return Py_BuildValue("s", VERSION);
}

static pyob *qinfo_get_thread_count(pyob *self)
{
  int sts;
  sts = get_thread_count();
  return Py_BuildValue("i", sts);
}
static pyob *qinfo_get_total_memory(pyob *self)
{
  int sts;
  sts = get_total_memory();
  return Py_BuildValue("i", sts);
}

static pyob *qinfo_get_avalible_memory(pyob *self)
{
  int sts;
  sts = get_avalible_memory();
  return Py_BuildValue("i", sts);
}

static pyob *qinfo_get_uptime(pyob *self)
{
  int sts;
  sts = get_uptime();
  return Py_BuildValue("l", sts);
}

static pyob *qinfo_get_cpu_model(pyob *self)
{
  char * sts;
  sts = get_cpu_model();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}

static pyob *qinfo_operating_system_name(pyob *self)
{
  char * sts;
  sts = get_operating_system_name();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}

static pyob *qinfo_get_board_model(pyob *self)
{
  char * sts;
  sts = get_board_model();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}

static pyob *qinfo_kuname(pyob *self)
{
  char * sts;
  sts = kuname();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}


static PyMethodDef qinfof[] = {
    {"version", (PyCFunction)version, METH_NOARGS, "Returns the version of qinfo being used."},
    {"core_count", qinfo_get_core_count, METH_NOARGS, "Returns the core count."},
    {"thread_count", qinfo_get_thread_count, METH_NOARGS, "Returns the thread count."},
    {"total_memory", qinfo_get_total_memory, METH_NOARGS, "Returns the total memory in kB."},
    {"avalible_memory", qinfo_get_avalible_memory, METH_NOARGS, "Returns the avalible memory in kB."},
    {"uptime", qinfo_get_uptime, METH_NOARGS, "Returns the uptime in seconds."},
    {"cpu_model", qinfo_get_cpu_model, METH_NOARGS, "Returns the cpu model as a string."},
    {"os_name", qinfo_operating_system_name, METH_NOARGS, "Returns the operating system name (distro name) as a string."},
    {"motherboard_model", qinfo_get_board_model, METH_NOARGS, "Returns the model name of the motherboard along with the manufacturer."},
    {"kernel_release", qinfo_kuname, METH_NOARGS, "Returns the release name of the kernel"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef qinfo = {
    PyModuleDef_HEAD_INIT,
    "qinfo",
    "Python bindings for qinfo",
    -1, // Global State
    qinfof};

// Initializing function

PyMODINIT_FUNC PyInit_qinfo(void)
{
  return PyModule_Create(&qinfo);
}