CXX = clang++
CXXFLAGS += -std=c++11
CXXFLAGS += `pkg-config --cflags --libs jsoncpp` 
prom = main
src = $(shell find ./ -name "*.cc")
deps = $(shell find ./ -name "*.h")
obj = $(src:%.cc=%.o)

all:$(prom) dependency
$(prom):$(obj)
	$(CXX) $(CXXFLAGS) -o $(prom) $(obj)

%.o: %.cc $(deps)
	$(CXX) $(CXXFLAGS) -c $< -o $@
dependency:headers
headers:
	$(CXX) $(CXXFLAGS) -MM  $(src) > headers
include headers

clean:
	rm -rf $(obj) $(prom) headers
