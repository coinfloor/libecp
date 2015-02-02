OS := $(shell uname -s)

CPPFLAGS := -std=c99 $(CPPFLAGS)
CFLAGS := -O3 -fPIC -fvisibility=hidden -ffunction-sections -fdata-sections -Wno-parentheses $(CFLAGS)
LDLIBS += -lgmp
ifeq ($(OS),Linux)
LDFLAGS := -Wl,-O1,--gc-sections $(LDFLAGS)
else
ifeq ($(OS),Darwin)
CPPFLAGS += -I/opt/local/include
LDFLAGS := -Wl,-dead_strip $(LDFLAGS) -L/opt/local/lib
endif
endif

.PHONY : all clean

all : libecp.so sign_secp224k1

clean :
	rm -f *.o libecp.so sign_secp224k1


ecp.o : ecp.c ecp.h

libecp.o : libecp.c libecp.h ecp.h

libecp.so : libecp.o ecp.o

sign_secp224k1.o : ecp.h

sign_secp224k1 : sign_secp224k1.o ecp.o


%.so : %.o
	$(LINK.o) -shared $^ $(LOADLIBES) $(LDLIBS) -o $@
