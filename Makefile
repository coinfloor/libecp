OS := $(shell uname -s)

CPPFLAGS := -std=c99 $(CPPFLAGS)
CFLAGS := -O3 -fPIC -fvisibility=hidden -ffunction-sections -fdata-sections -Wno-parentheses $(CFLAGS)
LDLIBS += -lgmp
ifeq ($(OS),Linux)
LDFLAGS := -Wl,-O1,--gc-sections,--strip-all $(LDFLAGS)
else
ifeq ($(OS),Darwin)
CPPFLAGS += -I/opt/local/include
LDFLAGS := -Wl,-dead_strip $(LDFLAGS) -L/opt/local/lib
endif
endif

W64_CC := x86_64-w64-mingw32-gcc
W64_CFLAGS := $(filter-out -fPIC,$(CFLAGS))
W64_LDFLAGS := $(LDFLAGS)
W64_OBJDIR := out.w64

.PHONY : all clean

all : libecp.so sign_secp224k1

clean :
	rm -rf *.o libecp.so sign_secp224k1 $(W64_OBJDIR) sign_secp224k1.exe


ecp.o $(W64_OBJDIR)/ecp.o : ecp.c ecp.h

libecp.o : libecp.c libecp.h ecp.h

libecp.so : libecp.o ecp.o

sign_secp224k1.o $(W64_OBJDIR)/sign_secp224k1.o : sign_secp224k1.c ecp.h

sign_secp224k1 : sign_secp224k1.o ecp.o

sign_secp224k1.exe : $(addprefix $(W64_OBJDIR)/,sign_secp224k1.o ecp.o)


%.so : %.o
	$(LINK.o) -shared $^ $(LOADLIBES) $(LDLIBS) -o $@

$(W64_OBJDIR)/%.o : CC := $(W64_CC)
$(W64_OBJDIR)/%.o : CFLAGS := $(W64_CFLAGS)
$(W64_OBJDIR)/%.o : %.c
	mkdir -p $(W64_OBJDIR) && $(COMPILE.c) $(OUTPUT_OPTION) $<

%.exe : CC := $(W64_CC)
%.exe : LDFLAGS := $(W64_LDFLAGS)
%.exe : $(W64_OBJDIR)/%.o
	$(LINK.o) -static-libgcc $^ $(LOADLIBES) $(LDLIBS) -o $@
