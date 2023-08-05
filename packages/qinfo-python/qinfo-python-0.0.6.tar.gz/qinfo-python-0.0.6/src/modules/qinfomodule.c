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
  char *sts;
  sts = get_cpu_model();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}

static pyob *qinfo_operating_system_name(pyob *self)
{
  char *sts;
  sts = get_operating_system_name();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}

static pyob *qinfo_get_board_model(pyob *self)
{
  char *sts;
  sts = get_board_model();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}

static pyob *qinfo_kuname(pyob *self)
{
  char *sts;
  sts = kuname();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}

static pyob *qinfo_parse_config(pyob *self, pyob *args)
{
  char *config_location;
  bool silent;
  configuration config;
  if (!PyArg_ParseTuple(args, "sB", &config_location, &silent))
  {
    return NULL;
  }

  if (parse_config(&config, config_location, silent) != 0)
  {
    return NULL;
  }
  pyob *display_cpu = Py_BuildValue("B", config.DISPLAY_CPU_INFO);
  pyob *display_etc = Py_BuildValue("B", config.DISPLAY_ETC_CPU_INFO);
  pyob *display_mem = Py_BuildValue("B", config.DISPLAY_MEMORY_INFO);
  pyob *display_board = Py_BuildValue("B", config.DISPLAY_MOTHERBOARD_INFO);
  pyob *display_hostname = Py_BuildValue("B", config.DISPLAY_HOSTNAME);
  pyob *display_uptime = Py_BuildValue("B", config.DISPLAY_UPTIME);
  pyob *display_os = Py_BuildValue("B", config.DISPLAY_OPERATING_SYSTEM);
  pyob *display_gb = Py_BuildValue("B", config.USE_GIGABYTES);
  pyob *display_kern = Py_BuildValue("B", config.DISPLAY_KERNEL_VERSION);
  pyob *display_logo = Py_BuildValue("B", config.DISPLAY_LOGO);
  pyob *display_rootfs = Py_BuildValue("B", config.DISPLAY_ROOTFS_BIRTHDAY);
  pyob *display_dates = Py_BuildValue("B", config.DISPLAY_DATES_YYYY_MM_DD);
  pyob *display_username = Py_BuildValue("B", config.DISPLAY_USERNAME);
  pyob *display_pkg = Py_BuildValue("B", config.DISPLAY_PACKAGES);
  pyob *display_shell = Py_BuildValue("B", config.DISPLAY_SHELL);
  pyob *display_idcol = Py_BuildValue("s", config.IDCOLOR);
  pyob *display_txtcol = Py_BuildValue("s", config.TXTCOLOR);
  pyob *display_logocol = Py_BuildValue("s", config.LOGOCOLOR);

  pyob *dict = PyDict_New();
  PyDict_SetItemString(dict, "display_cpu", display_cpu);
  PyDict_SetItemString(dict, "display_etc_cpu", display_etc);
  PyDict_SetItemString(dict, "display_mem", display_mem);
  PyDict_SetItemString(dict, "display_board", display_board);
  PyDict_SetItemString(dict, "display_hostname", display_hostname);
  PyDict_SetItemString(dict, "display_uptime", display_uptime);
  PyDict_SetItemString(dict, "display_gb", display_gb);
  PyDict_SetItemString(dict, "display_kernel", display_kern);
  PyDict_SetItemString(dict, "display_logo", display_logo);
  PyDict_SetItemString(dict, "display_rootfs_birth", display_rootfs);
  PyDict_SetItemString(dict, "display_pkg_count", display_pkg);
  PyDict_SetItemString(dict, "display_shell", display_cpu);
  PyDict_SetItemString(dict, "idcolor", display_idcol);
  PyDict_SetItemString(dict, "txtcolor", display_txtcol );
  PyDict_SetItemString(dict, "logocolor", display_logocol);
  
  return dict;
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
    {"kernel_release", qinfo_kuname, METH_NOARGS, "Returns the release name of the kernel."},
    {"parse_config", qinfo_parse_config, METH_VARARGS, "Returns a dict of all the configuration options."},
    {NULL, NULL, 0, NULL}
};

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