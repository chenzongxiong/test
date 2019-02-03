#include <iostream>
#include <stdlib.h>
#include <sys/sysinfo.h>
#include <sys/statvfs.h>
#include <errno.h>
#include <unistd.h>

int main() {
  struct sysinfo* sinfo = (struct sysinfo*)malloc(sizeof(struct sysinfo));
  int ret = 0;
  ret = sysinfo(sinfo);
  if (ret == EFAULT) {
    return 1;
  }
  std::cout << "sinfo->totalram: " << sinfo->totalram << " bytes" << std::endl;
  std::cout << "sinfo->freeram: " << sinfo->freeram << " bytes" << std::endl;
  std::cout << "sinfo->sharedram: " << sinfo->sharedram << " bytes" << std::endl;
  std::cout << "sinfo->bufferram: " << sinfo->bufferram << " bytes" << std::endl;
  std::cout << "sinfo->totalswap: " << sinfo->totalswap << " bytes" << std::endl;
  std::cout << "sinfo->freeswap: " << sinfo->freeswap << " bytes" << std::endl;
  std::cout << "sinfo->loads[0]: " << sinfo->loads[0] << " bytes" << std::endl;
  std::cout << "sinfo->loads[1]: " << sinfo->loads[1] << " bytes" << std::endl;
  std::cout << "sinfo->loads[2]: " << sinfo->loads[2] << " bytes" << std::endl;
  std::cout << "sinfo->totalhigh: " << sinfo->totalhigh << " bytes" << std::endl;
  std::cout << "sinfo->freehigh: " << sinfo->freehigh << " bytes" << std::endl;
  std::cout << "sinfo->mem_unit: " << sinfo->mem_unit << " bytes" << std::endl;
  std::cout << "sinfo->procs: " << sinfo->procs << std:: endl;

  std::cout << "nbr of processes configured: " << sysconf(_SC_NPROCESSORS_CONF) << std::endl;
  std::cout << "nbr of processes available: " << sysconf(_SC_NPROCESSORS_ONLN) << std::endl;

  struct statvfs *svfs = (struct statvfs*)malloc(sizeof(struct statvfs));
  ret = statvfs("/", svfs);
  std::cout << "svfs->f_bsize: " << svfs->f_bsize << std::endl;

  return 0;
}
