if HAVE_LOCAL_LIBFMOS
AM_CPPFLAGS = \
	-I$(top_srcdir)/include \
	-I$(top_srcdir)/common \
	@LIBCERROR_CPPFLAGS@ \
	@LIBCTHREADS_CPPFLAGS@ \
	@LIBCNOTIFY_CPPFLAGS@ \
	@PTHREAD_CPPFLAGS@ 

noinst_LTLIBRARIES = libfmos.la

libfmos_la_SOURCES = \
	libfmos_adc.c libfmos_adc.h \
	libfmos_definitions.h \
	libfmos_extern.h \
	libfmos_error.c libfmos_error.h \
	libfmos_libcerror.h \
	libfmos_libcnotify.h \
	libfmos_lzfse.c libfmos_lzfse.h \
	libfmos_lzfse_bit_stream.c libfmos_lzfse_bit_stream.h \
	libfmos_lzfse_decoder.c libfmos_lzfse_decoder.h \
	libfmos_lzvn.c libfmos_lzvn.h \
	libfmos_notify.c libfmos_notify.h \
	libfmos_support.c libfmos_support.h \
	libfmos_types.h \
	libfmos_unused.h
endif

MAINTAINERCLEANFILES = \
	Makefile.in

distclean: clean
	/bin/rm -f Makefile

splint:
	@echo "Running splint on libfmos ..."
	-splint -preproc -redef $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(libfmos_la_SOURCES)

