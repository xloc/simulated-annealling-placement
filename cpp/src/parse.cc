#include <sstream>
#include <iostream>
#include <vector>
#include <memory>

std::vector<std::vector<std::tuple<int, int>>> parse_nets(std::unique_ptr<std::istream> file)
{
  std::vector<std::vector<std::tuple<int, int>>> output;

  std::string line;
  int x, y;
  while (getline(*file, line))
  {
    std::istringstream line_stream(line);
    line_stream >> x >> y;
  }
}

int main()
{
  std::vector<std::string> strings;
  std::istringstream f("3 3 2 2\n3 0 1 2\n2 2 0\n2 1 2\n");
  std::string s;
  while (getline(f, s))
  {
    std::cout << s << std::endl;
    strings.push_back(s);
  }
}