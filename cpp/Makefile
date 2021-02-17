src = $(wildcard src/*.cc)
obj = $(src:.cc=.o)

CXXFLAGS = -Wall -g -std=c++11 -pthread

myprog: $(obj)
	$(CXX) $(LDFLAGS) -o $@ $^ $(LIBS)
	./$@

.PHONY: clean
clean:
	rm -f $(obj) myprog