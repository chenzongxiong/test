#include <sys/sysinfo.h>
#include <sys/statvfs.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>

#include "json.hpp"

using JSON = nlohmann::json;
// memory metrics
// struct sinfo {
//   long uptime;             /* Seconds since boot */
//   unsigned long loads[3];  /* 1, 5, and 15 minute load averages */
//   unsigned long totalram;  /* Total usable main memory size */
//   unsigned long freeram;   /* Available memory size */
//   unsigned long sharedram; /* Amount of shared memory */
//   unsigned long bufferram; /* Memory used by buffers */
//   unsigned long totalswap; /* Total swap space size */
//   unsigned long freeswap;  /* Swap space still available */
//   unsigned short procs;    /* Number of current processes */
//   unsigned long totalhigh; /* Total high memory size */
//   unsigned long freehigh;  /* Available high memory size */
//   unsigned int mem_unit;   /* Memory unit size in bytes */
//   char _f[20-2*sizeof(long)-sizeof(int)];  /* Padding to 64 bytes */
// };
// file system metrics
// struct statvfs {
//   unsigned long  f_bsize;    /* file system block size */
//   unsigned long  f_frsize;   /* fragment size */
//   fsblkcnt_t     f_blocks;   /* size of fs in f_frsize units */
//   fsblkcnt_t     f_bfree;    /* # free blocks */
//   fsblkcnt_t     f_bavail;   /* # free blocks for unprivileged users */
//   fsfilcnt_t     f_files;    /* # inodes */
//   fsfilcnt_t     f_ffree;    /* # free inodes */
//   fsfilcnt_t     f_favail;   /* # free inodes for unprivileged users */
//   unsigned long  f_fsid;     /* file system ID */
//   unsigned long  f_flag;     /* mount flags */
//   unsigned long  f_namemax;  /* maximum filename length */
// };
// cpu metrics
// read from /proc/stat
// TODO
// network metrics
typedef unsigned long uint64_t;

#define PROC_STAT_CPU_COLUMNS 11

struct cpuinfo {
  // std::string name;
  unsigned long user;
  unsigned long nice;
  unsigned long system;
  unsigned long idle;
  unsigned long iowait;
  unsigned long irq;
  unsigned long softirq;
  unsigned long steal;
  unsigned long guest;
  unsigned long guest_nice;
  char name[8];

  JSON load(std::string cpuInfoStr) {
    JSON cpu = JSON::parse(cpuInfoStr);
    return cpu;
  }
  JSON load() {
    JSON cpu;
    cpu["name"] = name;
    cpu["user"] = user;
    cpu["nice"] = nice;
    cpu["system"] = system;
    cpu["idle"] = idle;
    cpu["iowait"] = iowait;
    cpu["irq"] = irq;
    cpu["softirq"] = softirq;
    cpu["steal"] = steal;
    cpu["guest"] = guest;
    cpu["guest_nice"] = guest_nice;
    return cpu;
  }
  std::string dump() {
    JSON cpu;
    cpu["name"] = name;
    cpu["user"] = user;
    cpu["nice"] = nice;
    cpu["system"] = system;
    cpu["idle"] = idle;
    cpu["iowait"] = iowait;
    cpu["irq"] = irq;
    cpu["softirq"] = softirq;
    cpu["steal"] = steal;
    cpu["guest"] = guest;
    cpu["guest_nice"] = guest_nice;
    return cpu.dump();
  }
};

class Metrics {
public:
  Metrics() {
    this->sinfo = (struct sysinfo *)malloc(sizeof(struct sysinfo));
    this->svfs = (struct statvfs *)malloc(sizeof(struct statvfs));

    int ret;
    ret = sysinfo(this->sinfo);
    if (ret == EFAULT) {
      exit(1);
    }
    ret = statvfs("/", this->svfs);
    if (ret == EFAULT) {
      exit(1);
    }
    this->readProcStat();
    // this->nbrProcessors = sysconf( _SC_NPROCESSORS_ONLN );
    this->nbrProcessors = this->cinfoVec.size() - 1;
  }

  ~Metrics() {
    free(this->sinfo);
    free(this->svfs);
  }

  // static metrics
  uint64_t totalram() {
    return this->sinfo->totalram;
  }
  uint64_t totalswap() {
    return this->sinfo->totalswap;
  }
  uint64_t ncpus() {
    return this->nbrProcessors;
  }
  // dynamic metrics
  uint64_t uptime() {
    return this->sinfo->uptime;
  }
  uint64_t freeram() {
    return this->sinfo->freeram;
  }
  uint64_t freeswap() {
    return this->sinfo->freeswap;
  }
  uint64_t procs() {
    return this->sinfo->procs;
  }
  uint64_t bufferram() {
    return this->sinfo->bufferram;
  }
  uint64_t sharedram() {
    return this->sinfo->sharedram;
  }
  void print();
  std::string dump();
  JSON load(const char* metricsBuffer);

private:
  void readProcStat();

private:
  struct sysinfo* sinfo;
  struct statvfs* svfs;
  std::vector<struct cpuinfo*> cinfoVec;
  long nbrProcessors;
};
