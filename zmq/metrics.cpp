#include <iostream>
#include "metrics.hpp"


void Metrics::print() {
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

  std::cout << "nbr of processes available: " << nbrProcessors << std::endl;

  for (auto cpuinfo : this->cinfoVec) {
    std::cout << "========================================" << std::endl;
    std::cout << "cpuinfo->name: " << cpuinfo->name << std::endl;
    std::cout << "cpuinfo->user: " << cpuinfo->user << std::endl;
    std::cout << "cpuinfo->nice: " << cpuinfo->nice << std::endl;
    std::cout << "cpuinfo->system: " << cpuinfo->system << std::endl;
    std::cout << "cpuinfo->idle: " << cpuinfo->idle << std::endl;
    std::cout << "cpuinfo->iowait: " << cpuinfo->iowait << std::endl;
    std::cout << "cpuinfo->irq: " << cpuinfo->irq << std::endl;
    std::cout << "cpuinfo->softirq " << cpuinfo->softirq << std::endl;
    std::cout << "cpuinfo->steal: " << cpuinfo->steal << std::endl;
    std::cout << "cpuinfo->guest: " << cpuinfo->guest << std::endl;
    std::cout << "cpuinfo->guest_nice: " << cpuinfo->guest_nice << std::endl;
  }
}

void Metrics::readProcStat() {
  std::ifstream fileStat("/proc/stat");
  std::string line;
  std::string token;
  while (std::getline(fileStat, line)) {
    // line starts with "cpu"
    if (! line.compare(0, 3, "cpu")) {
      std::istringstream ss(line);
      std::vector<std::string> tokens{
        std::istream_iterator<std::string>{ss},
          std::istream_iterator<std::string>{}
      };

      // check columns
      if (tokens.size() != PROC_STAT_CPU_COLUMNS) {
        std::cout << "ERROR: /proc/stat incorrect" << std::endl;
      }
      struct cpuinfo* cinfo = (struct cpuinfo *)malloc(sizeof(struct cpuinfo));

      int len = tokens[0].copy(cinfo->name, tokens[0].size());
      cinfo->name[len] = '\0';
      cinfo->user = std::stoul(tokens[1]);
      cinfo->nice = std::stoul(tokens[2]);
      cinfo->system = std::stoul(tokens[3]);
      cinfo->idle = std::stoul(tokens[4]);
      cinfo->iowait = std::stoul(tokens[5]);
      cinfo->irq = std::stoul(tokens[6]);
      cinfo->softirq = std::stoul(tokens[7]);
      cinfo->steal = std::stoul(tokens[8]);
      cinfo->guest= std::stoul(tokens[9]);
      cinfo->guest_nice = std::stoul(tokens[10]);
      this->cinfoVec.push_back(cinfo);
    }
  }
  // sanity check
  // if (this->cinfoVec.size() != (this->nbrProcessors + 1)) {
  //   std::cout << "this->cinfoVec.size(): " << this->cinfoVec.size() << ", this->nbrProcessors: " << this->nbrProcessors << std::endl;
  //   std::cout << "ERROR: cpuinfo counts" << std::endl;
  // }
}

std::string Metrics::dump() {
  JSON m;
  JSON memory;
  memory["totalram"] = this->sinfo->totalram;
  memory["totalswap"] = this->sinfo->totalswap;
  memory["freeram"] = this->sinfo->freeram;
  memory["sharedram"] = this->sinfo->sharedram;
  memory["bufferram"] = this->sinfo->bufferram;
  memory["freeswap"] = this->sinfo->freeswap;
  memory["totalhigh"] = this->sinfo->totalhigh;
  memory["freehigh"] = this->sinfo->freehigh;
  memory["procs"] = this->sinfo->procs;
  memory["mem_unit"] = this->sinfo->mem_unit;
  memory["loads_1min"] = this->sinfo->loads[0];
  memory["loads_5min"] = this->sinfo->loads[1];
  memory["loads_15min"] = this->sinfo->loads[2];

  JSON fs;
  fs["f_bsize"] = this->svfs->f_bsize;
  fs["f_frsize"] = this->svfs->f_frsize;
  fs["f_blocks"] = this->svfs->f_blocks;
  fs["f_bfree"] = this->svfs->f_bfree;
  fs["f_bavail"] = this->svfs->f_bavail;

  JSON cpus;
  for (auto& cpu : this->cinfoVec) {
    cpus.push_back(cpu->load());
  }

  m["mem"] = memory;
  m["fs"] = fs;
  m["cpus"] = cpus;
  return m.dump();
}

JSON Metrics::load(const char* metricsBuffer) {
  JSON metrics = JSON::parse(metricsBuffer);
  return metrics;
}
