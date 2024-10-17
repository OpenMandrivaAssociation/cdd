Name:		cdd
Version:	094g
Release:	3
Summary:	A library for generating all vertices in convex polyhedrons
Group:		Sciences/Mathematics
License:	GPLv2+
Source0:	ftp://ftp.ifor.math.ethz.ch/pub/fukuda/cdd/cddlib-%{version}.tar.gz
# Extracted from http://www.sagemath.org/packages/standard/cddlib-094f.p11.spkg
Source1:        cdd_both_reps.c
Source2:	%{name}.rpmlintrc
URL:		https://www.ifor.math.ethz.ch/~fukuda/cdd_home/index.html
# Patch from sagemath to build and test cdd_both_reps
Patch0:         %{name}-sagemath.patch
# Create symbol aliases for the gmp build of cddlib.  This is needed by
# polymake, which links against both versions of cddlib, and needs some way to
# call functions in both.
Patch1:         %{name}-polymake.patch

BuildRequires:	libtool
BuildRequires:	gmp-devel
BuildRequires:	texlive

%description
The C-library cddlib is a C implementation of the Double Description 
Method of Motzkin et al. for generating all vertices (i.e. extreme points)
and extreme rays of a general convex polyhedron in R^d given by a system 
of linear inequalities:

   P = { x=(x1, ..., xd)^T :  b - A  x  >= 0 }

where A is a given m x d real matrix, b is a given m-vector 
and 0 is the m-vector of all zeros.

The program can be used for the reverse operation (i.e. convex hull
computation). This means that one can move back and forth between 
an inequality representation and a generator (i.e. vertex and ray) 
representation of a polyhedron with cdd. Also, cdd can solve a linear
programming problem, i.e. a problem of maximizing and minimizing 
a linear function over P.

%package	-n cddlib
Summary:	A library for generating all vertices in convex polyhedrons
Group:		Sciences/Mathematics

%description	-n cddlib
The C-library cddlib is a C implementation of the Double Description 
Method of Motzkin et al. for generating all vertices (i.e. extreme points)
and extreme rays of a general convex polyhedron in R^d given by a system 
of linear inequalities:

   P = { x=(x1, ..., xd)^T :  b - A  x  >= 0 }

where A is a given m x d real matrix, b is a given m-vector 
and 0 is the m-vector of all zeros.

%package	-n cddlib-devel
Summary:	Headers for cddlib
Group:		Development/C
Requires:	cddlib = %{EVRD}

%description	-n cddlib-devel
Include files for cddlib.

%prep
%setup -q -n cddlib-%{version}
%patch0 -p1
%patch1 -p1

# Regenerate Makefile.in files due to patched Makefile.am files
autoreconf -ifs
ln -s ../lib-src/gmpdef.h lib-src-gmp/gmpdef.h
ln -s ../lib-src/gmpundef.h lib-src-gmp/gmpundef.h

# Install sagemath extra source
cp -p %{SOURCE1} src
ln -sf ../src/cdd_both_reps.c src-gmp/cdd_both_reps.c

# Clean up the examples
rm -rf src/~ src-gmp/~
find . -name \.DS_Store\* | xargs rm -f
rm doc/cddlibman.{aux,blg,dvi,log,pdf,ps}

# Fix the FSF's address
for f in `find . -type f -print0 | xargs -0 grep -Fl '675 Mass'`; do
  sed -i.orig \
    's/675 Mass Ave, Cambridge, MA 02139/51 Franklin Street, Suite 500, Boston, MA  02110-1335/' \
    $f
  touch -r $f.orig $f
  rm -f $f.orig
done

find . -type f -exec chmod a+r {} \;
find . -type d -exec chmod a+rx {} \;

%build
%configure

# Get rid of undesirable hardcoded rpaths
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -i libtool

# Configure finds libgmp and tries to link it with everything.
sed -i 's/ -lgmp//' lib-src/Makefile

make %{?_smp_mflags}
cd doc
pdflatex cddlibman.tex
pdflatex cddlibman.tex

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
mkdir $RPM_BUILD_ROOT%{_includedir}/cddlib
mv $RPM_BUILD_ROOT%{_includedir}/{cdd,cdd_f,cddmp,cddmp_f,cddtypes,cddtypes_f,setoper}.h \
  $RPM_BUILD_ROOT%{_includedir}/cddlib/
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%files
%{_bindir}/*

%files -n cddlib
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/*.so.*

%files -n cddlib-devel
%doc doc/cddlibman.pdf examples*
%{_includedir}/cddlib
%{_libdir}/*.so
