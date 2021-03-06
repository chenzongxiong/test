#include "metrics.hpp"


int main() {

  Metrics *metrics = new Metrics();
  std::cout << "Serialize to String..." << std::endl;
  std::string metricStr = metrics->dump();
  std::cout << metricStr << std::endl;
  std::cout << "Deserialize String..." << std::endl;
  JSON m = metrics->load(metricStr.c_str());
  std::cout << m["mem"] << std::endl;

  // metrics->readNetworkStats();
  return 0;

}
