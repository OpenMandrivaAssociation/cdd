%define		cdddir		%{_datadir}/cdd
%define		cdd_version	0.61a
%define		cddxx_version	0.77a
%define		cddlib_version	0.94f
%define		libname		cddlib-devel

Name:		cdd
Group:		Sciences/Mathematics
License:	GPL
Summary:	Implementation of the Double Description Method of Motzkin et al
Version:	%{cdd_version}
Release:	%mkrel 5
Source0:	ftp://ftp.ifor.math.ethz.ch/pub/fukuda/cdd/cdd-061a.tar.gz
Source1:	ftp://ftp.ifor.math.ethz.ch/pub/fukuda/cdd/cdd+-077a.tar.gz
Source2:	ftp://ftp.ifor.math.ethz.ch/pub/fukuda/cdd/cddlib-094f.tar.gz
Source3:	cdd_both_reps.c
URL:		http://www.ifor.math.ethz.ch/~fukuda/cdd_home/index.html

Patch0:		cdd-g++4.2.patch
Patch1:		cdd-sagemath.patch

BuildRequires:	libgmp-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
The program cdd is a C implementation of the Double Description
Method of Motzkin et al. for generating all vertices (i.e. extreme points)
and extreme rays of a general convex polyhedron in R^d given by a system
of linear inequalities:

   P = { x :  A  x  <=  b }

where  A  is an m x d real matrix and b is a real m dimensional vector.
The program can be used for the reverse operation (i.e. convex hull
computation).  This means that  one can move back and forth between 
an inequality representation  and a generator (i.e. vertex and ray) 
representation of a polyhedron with cdd.  Also, cdd can solve a linear
programming problem, i.e. a problem of maximizing and minimizing 
a linear function over P.

########################################################################
%package	-n cdd+
Group:		Sciences/Mathematics
Summary:	Implementation of the Double Description Method of Motzkin et al
Version:	%{cddxx_version}
Requires:	%{name}

%description	-n cdd+
The program cdd+ is a C++ implementation of the Double Description 
Method of Motzkin et al. for generating all vertices (i.e. extreme points)
and extreme rays of a general convex polyhedron in R^d given by a system 
of linear inequalities:

   P = { x :  A  x  <=  b }

where  A  is an m x d real matrix and b is a real m dimensional vector.
The program can be used for the reverse operation (i.e. convex hull
computation) if one run cdd with "hull" option.  This means that 
one can move back and forth between an inequality representation 
and a generator (i.e. vertex and ray) representation of a polyhedron
with cdd+.  Also, cdd+ can solve a linear programming problem, i.e.
a problem of maximizing and minimizing a linear function over P.

########################################################################
%package	-n %{libname}
Group:		Development/C
Summary:	Implementation of the Double Description Method of Motzkin et al
Version:	%{cddlib_version}

%description	-n %{libname}
The C-library cddlib is a C implementation of the Double Description 
Method of Motzkin et al. for generating all vertices (i.e. extreme points)
and extreme rays of a general convex polyhedron in R^d given by a system 
of linear inequalities:

   P = { x=(x1, ..., xd)^T :  b - A  x  >= 0 }

where  A  is a given m x d real matrix, b is a given m-vector 
and 0 is the m-vector of all zeros.

########################################################################
%prep
%setup -q -D -c cdd -a0 -a1 -a2

pushd cddlib-094f
  cp %{SOURCE3} src
  cd src-gmp
  ln -sf ../src/cdd_both_reps.c .
popd

%patch0	-p1
%patch1	-p1

%build
pushd cddlib-094f
  autoreconf -ifs
  %configure --bindir=%{cdddir}/bin --includedir=%{_includedir}/%{name}
  %make gmpdir=%{_prefix}
popd

pushd cdd-061
  make CC=gcc all
  pushd utility
    make CC=gcc CFLAGS="%{optflags} -lm" all
  popd
popd

pushd cdd+-077a
  make					\
	CC=g++				\
	LIBDIR=%{_libdir}		\
	GMPLIBDIR=%{_libdir}		\
	GMPINCLUDEDIR=%{_includedir}	\
	OPTFLAGS="%{optflags}"		\
	all
popd

########################################################################
%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{cdddir}/bin

pushd cddlib-094f
  %makeinstall_std
  mkdir -p %{buildroot}/%{_docdir}/%{name} %{buildroot}/%{cdddir}/bin
  cp -fa src/cdd_both_reps src-gmp/cdd_both_reps_gmp 
  cp -fa doc/cddlibman.{dvi,pdf,ps} %{buildroot}/%{_docdir}/%{name}
  cp -fa examples{,-ext,-ine{,3d}}/ %{buildroot}/%{cdddir}
  cp -fa README %{buildroot}/%{_docdir}/%{name}/README.cddlib
popd

pushd cdd-061
  cp -fa cdd dplex_test utility/{delaunay,rlp,voronoi} %{buildroot}/%{cdddir}/bin
  cp -far ext/ ine/ %{buildroot}/%{cdddir}
  cp -fa cdd.readme %{buildroot}/%{_docdir}/%{name}
popd

pushd cdd+-077a
  cp -fa cddf+ cddr+ get_essential %{buildroot}/%{cdddir}/bin
  # Several files are duplicated from cdd-061
  cp -far ext/* %{buildroot}/%{cdddir}/ext
  cp -far ine/* %{buildroot}/%{cdddir}/ine
  cp -fa README.cdd+* cddman.dvi %{buildroot}/%{_docdir}/%{name}
popd

find %{buildroot} -type d -exec chmod a+x {} \;
find %{buildroot} -type f -exec chmod a+r {} \;

%clean
rm -rf %{buildroot}

########################################################################
%files
%defattr(-,root,root,-)
%dir %{cdddir}
%dir %{cdddir}/bin
%{cdddir}/bin/cdd
%{cdddir}/bin/cdd_both_reps
%{cdddir}/bin/cdd_both_reps_gmp
%{cdddir}/bin/dplex_test
%{cdddir}/bin/delaunay
%{cdddir}/bin/rlp
%{cdddir}/bin/voronoi
%dir %{cdddir}/ext
%{cdddir}/ext/ccc4.ext
%{cdddir}/ext/ccc5.ext
%{cdddir}/ext/ccc6.ext
%{cdddir}/ext/ccc7.ext
%{cdddir}/ext/ccp4.ext
%{cdddir}/ext/ccp5.ext
%{cdddir}/ext/ccp6.ext
%{cdddir}/ext/ccp7.ext
%{cdddir}/ext/irbox200-4.ext
%{cdddir}/ext/irbox20-4.ext
%{cdddir}/ext/prodst62.ext
%{cdddir}/ext/reg24-5.ext
%{cdddir}/ext/reg600-5.ext
%{cdddir}/ext/verifyinput1.ext
%dir %{cdddir}/ine
%{cdddir}/ine/cross10.ine
%{cdddir}/ine/cross12.ine
%{cdddir}/ine/cross6.ine
%{cdddir}/ine/cross8.ine
%{cdddir}/ine/cube10.ine
%{cdddir}/ine/cube12.ine
%{cdddir}/ine/cube14.ine
%{cdddir}/ine/cube16.ine
%{cdddir}/ine/cube6.ine
%{cdddir}/ine/cube8.ine
%{cdddir}/ine/ex1.ine
%{cdddir}/ine/findinter.ine
%{cdddir}/ine/infeas.ine
%{cdddir}/ine/integralpoints.ine
%{cdddir}/ine/lpmaxtest.ine
%{cdddir}/ine/lpmintest.ine
%{cdddir}/ine/lptableau.ine
%{cdddir}/ine/mit729-9.ine
%{cdddir}/ine/nonfull.ine
%{cdddir}/ine/origin.ine
%{cdddir}/ine/partialtest1.ine
%{cdddir}/ine/partialtest2.ine
%{cdddir}/ine/prodmT5.ine
%{cdddir}/ine/projtest.ine
%{cdddir}/ine/ucube.ine
%{cdddir}/ine/verifyinput2.ine
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/cdd.readme

%files		-n cdd+
%defattr(-,root,root,-)
%dir %{cdddir}
%{cdddir}/bin/cddf+
%{cdddir}/bin/cddr+
%{cdddir}/bin/get_essential
%{cdddir}/ext/accuracy.ext
%{cdddir}/ext/cyclic10-4.ext
%{cdddir}/ext/cyclic12-6.ext
%{cdddir}/ext/cyclic14-8.ext
%{cdddir}/ext/cyclic16-10.ext
%{cdddir}/ext/postcdd.ext
%{cdddir}/ext/vertextest.ext
%{cdddir}/ine/facettest1.ine
%{cdddir}/ine/facettest2.ine
%{cdddir}/ine/kkd18_4.ine
%{cdddir}/ine/kkd27_5.ine
%{cdddir}/ine/kkd38_6.ine
%{cdddir}/ine/multiplerows.ine
%{cdddir}/ine/rational.ine
%{cdddir}/ine/topetest1.ine
%{cdddir}/ine/topetest2.ine
%{cdddir}/ine/topetest3.ine
%doc %{_docdir}/%{name}/cddman.dvi
%doc %{_docdir}/%{name}/README.cdd+*

%files		-n %{libname}
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/libcdd.a
%{_libdir}/libcddgmp.a
%{cdddir}/bin/adjacency
%{cdddir}/bin/adjacency_gmp
%{cdddir}/bin/allfaces
%{cdddir}/bin/allfaces_gmp
%{cdddir}/bin/fourier
%{cdddir}/bin/fourier_gmp
%{cdddir}/bin/lcdd
%{cdddir}/bin/lcdd_gmp
%{cdddir}/bin/projection
%{cdddir}/bin/projection_gmp
%{cdddir}/bin/redcheck
%{cdddir}/bin/redcheck_gmp
%{cdddir}/bin/scdd
%{cdddir}/bin/scdd_gmp
%{cdddir}/bin/testcdd1
%{cdddir}/bin/testcdd1_gmp
%{cdddir}/bin/testcdd2
%{cdddir}/bin/testcdd2_gmp
%{cdddir}/bin/testlp1
%{cdddir}/bin/testlp1_gmp
%{cdddir}/bin/testlp2
%{cdddir}/bin/testlp2_gmp
%{cdddir}/bin/testlp3
%{cdddir}/bin/testlp3_gmp
%{cdddir}/bin/testshoot
%{cdddir}/bin/testshoot_gmp
%dir %{cdddir}/examples
%{cdddir}/examples/*
%dir %{cdddir}/examples-ext
%{cdddir}/examples-ext/*
%dir %{cdddir}/examples-ine
%{cdddir}/examples-ine/*
%dir %{cdddir}/examples-ine3d
%{cdddir}/examples-ine3d/*
%doc %{_docdir}/%{name}/cddlibman.*
%doc %{_docdir}/%{name}/README.cddlib
