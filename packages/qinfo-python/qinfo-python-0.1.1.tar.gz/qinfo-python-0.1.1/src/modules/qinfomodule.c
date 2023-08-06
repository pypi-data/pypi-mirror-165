#include <Python.h>
#include "../../qinfo/src/unix.h"
#include "../../qinfo/src/config.h"
#include "../../qinfo/src/logo.h"

typedef PyObject pyob;

struct packages
{
  packagecount pacman_packages;
  packagecount apt_packages;
  packagecount apk_packages;
  packagecount flatpak_packages;
  packagecount snap_packages;
};

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
  long sts;
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
  char *os_name;
  if ((os_name = get_operating_system_name_bedrock()) == NULL)
  {
    os_name = get_operating_system_name();
  }

  pyob *retval = Py_BuildValue("s", os_name);
  free(os_name);
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

static pyob *qinfo_hostname(pyob *self)
{
  char *sts;
  sts = get_hostname();
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
  PyDict_SetItemString(dict, "display_shell", display_shell);
  PyDict_SetItemString(dict, "display_username", display_username);
  PyDict_SetItemString(dict, "display_os", display_os);
  PyDict_SetItemString(dict, "date_order", display_dates);
  PyDict_SetItemString(dict, "idcolor", display_idcol);
  PyDict_SetItemString(dict, "txtcolor", display_txtcol);
  PyDict_SetItemString(dict, "logocolor", display_logocol);

  return dict;
}

static pyob *qinfo_get_rootfs_fsage(pyob *self)
{
  struct date rootfsage = get_creation_date();

  pyob *year = Py_BuildValue("i", rootfsage.year);
  pyob *month = Py_BuildValue("i", rootfsage.month);
  pyob *day = Py_BuildValue("i", rootfsage.day);
  pyob *dict = PyDict_New();
  PyDict_SetItemString(dict, "year", year);
  PyDict_SetItemString(dict, "month", month);
  PyDict_SetItemString(dict, "day", day);

  return dict;
}

static struct packages formatted_packages(packagecount pacman_packages,
                                          packagecount apt_packages,
                                          packagecount apk_packages,
                                          packagecount flatpak_packages,
                                          packagecount snap_packages)
{
  struct packages pkgs;
  if (pacman_packages > 0)
  {
    pkgs.pacman_packages = pacman_packages;
  }
  else
  {
    pkgs.pacman_packages = 0;
  }
  if (apt_packages > 0)
  {
    pkgs.apt_packages = apt_packages;
  }
  else
  {
    pkgs.apt_packages = 0;
  }
  if (apk_packages > 0)
  {
    pkgs.apk_packages = apk_packages;
  }
  else
  {
    pkgs.apk_packages = 0;
  }
  if (flatpak_packages > 0)
  {
    pkgs.flatpak_packages = flatpak_packages;
  }
  else
  {
    pkgs.flatpak_packages = 0;
  }
  if (snap_packages > 0)
  {
    pkgs.snap_packages = snap_packages;
  }
  else
  {
    pkgs.snap_packages = 0;
  }
  return pkgs;
}

static pyob *qinfo_get_packages(pyob *self)
{
  struct packages pkgs;
  packagecount pacman_packages = 0;
  packagecount apt_packages = 0;
  packagecount apk_packages = 0;
  packagecount flatpak_packages = 0;
  packagecount snap_packages = 0;
  flatpak_packages = get_num_packages(FLATPAK_PACKAGE_MANAGER);
  snap_packages = get_num_packages(SNAP_PACKAGE_MANAGER);
  pacman_packages = get_num_packages(PACMAN_PACKAGE_MANAGER);
  apt_packages = get_num_packages(APT_PACKAGE_MANAGER);
  apk_packages = get_num_packages(APK_PACKAGE_MANAGER);
  pkgs = formatted_packages(pacman_packages, apt_packages, apk_packages,
                            flatpak_packages, snap_packages);

  pyob *py_pacman_packages = Py_BuildValue("i", pkgs.pacman_packages);
  pyob *py_apt_packages = Py_BuildValue("i", pkgs.apt_packages);
  pyob *py_apk_packages = Py_BuildValue("i", pkgs.apk_packages);
  pyob *py_flatpak_packages = Py_BuildValue("i", pkgs.flatpak_packages);
  pyob *py_snap_packages = Py_BuildValue("i", pkgs.snap_packages);

  pyob *dict = PyDict_New();
  PyDict_SetItemString(dict, "pacman", py_pacman_packages);
  PyDict_SetItemString(dict, "apt", py_apt_packages);
  PyDict_SetItemString(dict, "apk", py_apk_packages);
  PyDict_SetItemString(dict, "flatpak", py_flatpak_packages);
  PyDict_SetItemString(dict, "snap", py_snap_packages);
  
  return dict;
}

static pyob *qinfo_username(pyob *self)
{
  char *sts;
  sts = get_username();
  pyob *retval = Py_BuildValue("s", sts);
  return retval;
}

static pyob *qinfo_shell(pyob *self)
{
  char *sts;
  sts = get_shell_name();
  pyob *retval = Py_BuildValue("s", sts);
  free(sts);
  return retval;
}

static pyob *qinfo_logo(pyob *self)
{
  char *os_name;
  char *logo;
  if ((os_name = get_operating_system_name_bedrock()) == NULL)
  {
    os_name = get_operating_system_name();
  }
  if (strcmp(os_name, "Arch Linux") == 0)
  {
    logo = logo_arch;
  }
  else if (strstr(os_name, "Alpine Linux") != NULL)
  {
    logo = alpine_logo;
  }
  else if (strstr(os_name, "Arco Linux") != NULL)
  {
    logo = arcolinux_logo;
  }
  else if (strstr(os_name, "Aritx Linux") != NULL)
  {
    logo = artix_logo;
  }
  else if (strstr(os_name, "Bedrock Linux") != NULL)
  {
    logo = bedrock_logo;
  }
  else if (strstr(os_name, "Gentoo") != NULL)
  {
    logo = gentoo_logo;
  }
  else if (strstr(os_name, "Ubuntu") != NULL)
  {
    logo = ubuntu_logo;
  }
  else
  {
    logo = generic_logo;
  }
  free(os_name);

  pyob *retval = Py_BuildValue("s", logo);
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
    {"kernel_release", qinfo_kuname, METH_NOARGS, "Returns the release name of the kernel."},
    {"parse_config", qinfo_parse_config, METH_VARARGS, "Returns a dict of all the configuration options."},
    {"rootfs_age", qinfo_get_rootfs_fsage, METH_NOARGS, "Returns a dict of the age of the root file system."},
    {"username", qinfo_username, METH_NOARGS, "Returns the username of the user running the program as a string."},
    {"packages", qinfo_get_packages, METH_NOARGS, "Returns a dict of the number of packages for each supported package manager."},
    {"shell", qinfo_shell, METH_NOARGS, "Returns a string containing the shell (or if none found, the calling process)."},
    {"hostname", qinfo_hostname, METH_NOARGS, "Return the hostname of the system as a string."},
    {"logo", qinfo_logo, METH_NOARGS, "Return a string of the logo representing the distro."},
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