<TeXmacs|1.0.7.9>

<style|article>

<\body>
  <doc-data|<doc-title|Maniac>||<doc-author-data|<author-name|nicolas
  benoit>|<\author-address>
    nbenoit@tuxfamily.org

    \;
  </author-address>>|<\doc-date>
    Version 1.0.1 - <date>

    \;
  </doc-date>>

  \;

  <\abstract>
    This manual describes Maniac, a tool designed to automate the validation
    and the comparison of multiple variants of a same program. This goal is
    achieved by compiling each variant in a distinct shared object and
    generating a program that will successively load and execute them.
  </abstract>

  \;

  <\table-of-contents|toc>
    <vspace*|1fn><with|font-series|bold|math-font-series|bold|1<space|2spc>Introduction>
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-1><vspace|0.5fn>

    <with|par-left|1.5fn|1.1<space|2spc>Motivation
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-2>>

    <with|par-left|1.5fn|1.2<space|2spc>Concepts
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-3>>

    <with|par-left|3fn|1.2.1<space|2spc>Variant
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-4>>

    <with|par-left|3fn|1.2.2<space|2spc>Generator
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-5>>

    <with|par-left|3fn|1.2.3<space|2spc>Plan
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-6>>

    <with|par-left|3fn|1.2.4<space|2spc>Loader
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-7>>

    <vspace*|1fn><with|font-series|bold|math-font-series|bold|2<space|2spc>Quickstart>
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-8><vspace|0.5fn>

    <with|par-left|1.5fn|2.1<space|2spc>Installation
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-9>>

    <with|par-left|1.5fn|2.2<space|2spc>Usage & Behavior
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-10>>

    <with|par-left|1.5fn|2.3<space|2spc>Command-line Options
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-11>>

    <vspace*|1fn><with|font-series|bold|math-font-series|bold|3<space|2spc>Mania
    Description Files> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-13><vspace|0.5fn>

    <with|par-left|1.5fn|3.1<space|2spc>Environment Description
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-14>>

    <with|par-left|3fn|3.1.1<space|2spc>Generator Description
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-15>>

    <with|par-left|6fn|Cleaning <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-17><vspace|0.15fn>>

    <with|par-left|6fn|Checking <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-18><vspace|0.15fn>>

    Builtin Generators <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-19><vspace|0.15fn>

    <with|par-left|3fn|3.1.2<space|2spc>Variant Description
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-20>>

    <with|par-left|3fn|3.1.3<space|2spc>Plan Description
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-21>>

    <with|par-left|6fn|Builtin Plans <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-22><vspace|0.15fn>>

    <with|par-left|6fn|External Commands <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-23><vspace|0.15fn>>

    <with|par-left|1.5fn|3.2<space|2spc>Program Description
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-25>>

    <with|par-left|3fn|3.2.1<space|2spc>Extra Source File
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-26>>

    <with|par-left|3fn|3.2.2<space|2spc>Data List
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-27>>

    <with|par-left|6fn|Scalar <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-30><vspace|0.15fn>>

    <with|par-left|6fn|Array <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-31><vspace|0.15fn>>

    <with|par-left|6fn|Structure and Union
    <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
    <no-break><pageref|auto-32><vspace|0.15fn>>
  </table-of-contents>

  <new-page>

  <section|Introduction>

  Maniac helps to automate the validation and the comparison of multiple
  variants of a program.

  <subsection|Motivation>

  Writing a testsuite or benchmarks for code generation tools often requires
  a lot of code that is not stricly part of the routine studied, for example
  trace checking, data verification or timing. Many testsuites embed those
  utilities in a library to avoid code duplication. However the code gluing
  the library and the testcase is left to the developer/tester.

  Maniac was written from the point of view that the developer/tester should
  focus only on the testcase design. To this end, it automatically generates
  programs that will initialize data, call the testcase and check data
  against the ones generated by a reference implementation.

  <subsection|Concepts>

  This subsection explains the names given to the concepts Maniac deals with.

  <subsubsection|Variant>

  A variant is an implementation of a given algorithm.

  <subsubsection|Generator>

  A generator is a program that will generate a variant of an input source
  file.

  <subsubsection|Plan>

  A plan is a list of variants to process by Maniac. For each variant, a plan
  specifies if it has to be generated, checked, timed or whatever.

  <subsubsection|Loader>

  A loader is a program generated by Maniac that will call the variants of
  the studied routine.

  <section|Quickstart>

  This section explains how to install and run Maniac.

  <subsection|Installation>

  Maniac is a Python script. In order to run it from the command-line, you
  can either copy it in one of the directories of your PATH, or add Maniac
  directory to it. One of the following command should suffice :

  \;

  <\code*>
    $ cp maniac.py $HOME/.local/bin/maniac

    \;

    $ sudo cp maniac.py /usr/bin/maniac
  </code*>

  <subsection|Usage & Behavior>

  Through the command-line, the user specifies which directories Maniac
  should inspect and which plan(s) it should follow, each directory is
  assumed to contain a single program. According to the selected plan, Maniac
  first generates the variants. Then, it compiles each variant in a distinct
  shared object, and finally generates a source file which will sequentially
  load, initialize, run, time and/or check the variants' shared objects.
  After each plan, Maniac outputs a log of the whole process. It can also
  output this log to an HTML file.

  Maniac comes with a few demos :

  \;

  <\code*>
    $ cd demos/compiler options
  </code*>

  \;

  Try them out and read their Mania files to understand how it works.

  <subsection|Command-line Options>

  The command-line options related to Maniac are listed in table
  <reference|cmdoptions>

  <big-table|<block*|<tformat|<table|<row|<cell|<strong|Option>>|<cell|<strong|Long
  Option>>|<cell|<strong|Purpose>>>|<row|<cell|-G>|<cell|--nogen>|<cell|Disable
  generation of variants>>|<row|<cell|-m M>|<cell|--mania=M>|<cell|Look in
  the provided file for mania description>>|<row|<cell|-n
  N>|<cell|--numrpt=N>|<cell|Repeat each plan N times>>|<row|<cell|-o
  O>|<cell|--output=O>|<cell|Output HTML report to file named
  O>>>>>|Command-line options<label|cmdoptions>>

  <section|Mania Description Files>

  In order to proceed, Maniac requires the definition of an environment and a
  program in so-called <em|mania> files.

  Mania files are named 'mania.xml' by convention. A mania file can contain
  both environment and program descriptions. When Maniac is invoked, it first
  searches for environment description. The search order is the following :
  current directory, directories passed as arguments, parent directories.
  Once the environment is loaded, Maniac looks for program description as
  follow : current directory and directories passed as arguments.

  <subsection|Environment Description>

  The environment describes the variant generators, the variants and the
  plans.

  <subsubsection|Generator Description>

  The section describing the available generators is named <em|generators>.

  For each generator, the attributes are the following :

  <big-table|<block*|<tformat|<twith|table-lborder|1>|<twith|table-rborder|1>|<twith|table-bborder|1>|<twith|table-tborder|1>|<table|<row|<cell|<strong|Attribute>>|<cell|<strong|Purpose>>>|<row|<cell|name>|<cell|Name
  under which the generator will be referenced (reserved: none,
  copy)>>|<row|<cell|bin>|<cell|The absolute or relative path to the
  executable of the generator >>|<row|<cell|flags>|<cell|The flags to use
  when invoking the generator>>>>>|Generator Attributes>

  Here is an example of a generator description for Pocc (more info at
  <with|font-family|tt|http://pocc.sf.net>) :

  <\with|font-family|tt>
    <\with|font-base-size|8>
      \<less\>generators\<gtr\>

      \ \ \<less\>generator name=''pocc-tile'' bin=''pocc'' flags=''--pluto
      --pluto-tile -o %prog%-tile.c'' /\<gtr\>

      \<less\>/generators\<gtr\>
    </with>
  </with>

  \;

  <paragraph|Cleaning>

  For each generator, it is possible to set a list of files that should be
  rmeoved when the cleaning plan is requested. The syntax is the following :

  <with|font-base-size|8|<\with|font-family|tt>
    \<less\>cleans\<gtr\>

    \ \ \<less\>clean files=''file.tmp intermed.txt'' /\<gtr\>

    \<less\>/cleans\<gtr\>
  </with>>

  <new-page*><paragraph|Checking>

  After a generation step, a diff command can be invoked to check the output
  of some generation trace against a reference file. The syntax is the
  following :

  <\with|font-family|tt>
    <\with|font-base-size|8>
      \<less\>checks\<gtr\>

      \ \ \<less\>check name=''debug'' file=''%prog%-gen-debug'' /\<gtr\>

      \ \ \<less\>check name=''log'' file=''generation.log'' /\<gtr\>

      \<less\>/checks\<gtr\>
    </with>
  </with>

  \;

  <subparagraph|Builtin Generators>

  Two generators are currently defined by default.

  The <em|none> generator does nothing and should be used when the variant
  source file is not generated by an external program.

  The <em|copy> generator creates a copy of the reference program (actually a
  symlink).

  <subsubsection|Variant Description>

  Variants are defined within the <em|variants> section of the environment
  description. Usually, only two attributes are required : a name and the
  name of the generator that should be invoked to produce it.

  Note: the variant name <em|ref> is reserved for the original version of the
  program.

  <subsubsection|Plan Description>

  Plans are defined within the <em|plans> section of the environment
  description. A plan generally consist of a list of variants. For each
  variant, it possible to specify:

  <\itemize-dot>
    <item>compilation flags with the <em|compflags> attribute ;

    <item>wether the variant should be timed or not with the <em|time>
    attribute ;

    <item>wether the variant's data should be checked or not with the
    <em|chk> attribute.
  </itemize-dot>

  \;

  <paragraph|Builtin Plans>

  A plan named <em|clean> is defined by default. It will remove all generated
  and intermediate files for all variants defined in the environment.

  A plan named <em|ref> is also defined by default. It will invoke the
  generators and rename the <em|checks> files so they are used as a
  comparison basis for future generations.

  \;

  <paragraph|External Commands>

  Within a plan, it possible to replace or wrap some Maniac actions with
  external scripts. This is useful when the generated variants should be
  compiler and/or executed on an another computer.

  External commands shall be defined in a <em|commands> node within a plan.

  <big-table|<block*|<tformat|<table|<row|<cell|<strong|Name>>|<cell|<strong|Purpose>>>|<row|<cell|compile_variant>|<cell|Invokes
  a compiler for a variant source file provided as an
  argument.>>|<row|<cell|compile_loader>|<cell|Invokes a compiler for a
  loader source file provided as an argument.>>|<row|<cell|run_loader>|<cell|Invokes
  the loader binary provided as an argument.>>>>>|External command hooks>

  Example :

  <with|font-base-size|8|<\with|font-family|tt>
    \<less\>plan name=''extern_test''\<gtr\>

    \ \ \<less\>variants\<gtr\>

    \ \ \ \ \<less\>variant name=''ref'' /\<gtr\>

    \ \ \ \ \<less\>variant name=''tiled'' gen=''pocc-tile'' /\<gtr\>

    \ \ \<less\>/variants\<gtr\>

    \ \ \<less\>commands\<gtr\>

    \ \ \ \ \<less\>command id=''run_loader'' cmd=''send-and-run-loader.sh''
    /\<gtr\>

    \ \ \<less\>/commands\<gtr\>

    \<less\>/plan\<gtr\>
  </with>>

  <subsection|Program Description>

  The program description contains the program file name, the entry function
  name and its arguments, and the global variables the program accesses.

  The <em|program> node has two attributes : a <em|name> and a filename
  extension (``c'' is the default).

  The <em|entry> node has one attribute : the <em|name> of the entry function
  for the input program.

  \;

  Example :

  <with|font-base-size|8|<\with|font-family|tt>
    \<less\>program name=''program'' ext=''c''\<gtr\>

    \ \ \<less\>entry name=''main'' /\<gtr\>

    \<less\>/program\<gtr\>
  </with>>

  <subsubsection|Extra Source File>

  It is possible to add extra source files to a program using the
  <em|extrafile> node. Those are not processed by the generators, they are
  only used during the compilation of each variant.

  There can be as many extrafile nodes as you wish.

  \;

  Example :

  <with|font-base-size|8|<\with|font-family|tt>
    \<less\>program name=''program'' ext=''c''\<gtr\>

    \ \ \<less\>extrafile name=''program_extra.c'' /\<gtr\>

    \ \ \<less\>/entry name=''main'' /\<gtr\>

    \<less\>/program\<gtr\>
  </with>>

  <subsubsection|Data List>

  An entry node and a program node can contain a data node which is a list of
  data to initialize and/or check. Note that the data list attached to an
  entry node corresponds to the entry function parameters.

  <big-table|<block*|<tformat|<table|<row|<cell|<strong|Name>>|<cell|<strong|Purpose>>>|<row|<cell|type>|<cell|The
  type of the data, for example int, double, ...>>|<row|<cell|name>|<cell|The
  name of the data>>|<row|<cell|ini>|<cell|Indicates wether or not the data
  should be initialized>>|<row|<cell|value>|<cell|Describes the initial value
  of the data>>|<row|<cell|chk>|<cell|Indicates wether or not the data should
  be checked after the execution>>>>>|Data attributes>

  In order to describe the initial value of a data, the user can use
  arithmetic expressions. It is possible to access special values into those
  expressions :

  <big-table|<block*|<tformat|<table|<row|<cell|<strong|Name>>|<cell|<strong|Purpose>>>|<row|<cell|index>|<cell|A
  value corresponding to the index of an element in array data
  >>|<row|<cell|rand>|<cell|A random value>>>>>|Special values>

  \;

  <paragraph|Scalar>

  Scalar data are simple variables.

  Example :

  <with|font-base-size|8|<with|font-family|tt|\<less\>scalar type=''double''
  name=''var'' ini=''true'' value=''(rand+1)%76'' /\<gtr\>>>

  \;

  <paragraph|Array>

  Array data have the same attribute as other data, but require also the
  definition of a <em|dims> attribute that hold the dimensions of the array.

  Example for an array <em|A> declared as int A[16][16] :

  <with|font-base-size|8|<with|font-family|tt|\<less\>array type=''int''
  name=''A'' dims=''[16,16]'' /\<gtr\>>>

  \;

  <paragraph|Structure and Union>

  Structured and united data have the same attributes as other data but embed
  a data list which described the content of the structure.

  Beware, the type attribute corresponds to the name of the structure while
  the name attribute refers to the name a variable which type is the
  structure itsef.

  Example for a structure containing two integers :

  <with|font-base-size|8|<\with|font-family|tt>
    \<less\>struct type=''point'' name=''p1''\<gtr\>

    \ \ \<less\>data\<gtr\>

    \ \ \ \ \<less\>scalar type=''int'' name=''x'' /\<gtr\>

    \ \ \ \ \<less\>scalar type=''int'' name=''y'' /\<gtr\>

    \ \ \<less\>/data\<gtr\>

    \<less\>/struct\<gtr\>
  </with>>

  \;
</body>

<\initial>
  <\collection>
    <associate|page-medium|paper>
    <associate|par-hyphen|normal>
    <associate|sfactor|6>
  </collection>
</initial>

<\references>
  <\collection>
    <associate|api|<tuple|3.4.3|13>>
    <associate|auto-1|<tuple|1|2>>
    <associate|auto-10|<tuple|2.2|2>>
    <associate|auto-11|<tuple|2.3|3>>
    <associate|auto-12|<tuple|1|3>>
    <associate|auto-13|<tuple|3|3>>
    <associate|auto-14|<tuple|3.1|3>>
    <associate|auto-15|<tuple|3.1.1|3>>
    <associate|auto-16|<tuple|2|3>>
    <associate|auto-17|<tuple|3.1.1.1|3>>
    <associate|auto-18|<tuple|3.1.1.2|4>>
    <associate|auto-19|<tuple|3.1.1.2.1|4>>
    <associate|auto-2|<tuple|1.1|2>>
    <associate|auto-20|<tuple|3.1.2|4>>
    <associate|auto-21|<tuple|3.1.3|4>>
    <associate|auto-22|<tuple|3.1.3.1|4>>
    <associate|auto-23|<tuple|3.1.3.2|4>>
    <associate|auto-24|<tuple|3|4>>
    <associate|auto-25|<tuple|3.2|5>>
    <associate|auto-26|<tuple|3.2.1|5>>
    <associate|auto-27|<tuple|3.2.2|5>>
    <associate|auto-28|<tuple|4|5>>
    <associate|auto-29|<tuple|5|5>>
    <associate|auto-3|<tuple|1.2|2>>
    <associate|auto-30|<tuple|3.2.2.1|5>>
    <associate|auto-31|<tuple|3.2.2.2|5>>
    <associate|auto-32|<tuple|3.2.2.3|6>>
    <associate|auto-33|<tuple|3.6|14>>
    <associate|auto-34|<tuple|4|14>>
    <associate|auto-35|<tuple|4.1|14>>
    <associate|auto-36|<tuple|4.2|14>>
    <associate|auto-37|<tuple|4.3|15>>
    <associate|auto-38|<tuple|4.3.1|15>>
    <associate|auto-39|<tuple|4.3.2|15>>
    <associate|auto-4|<tuple|1.2.1|2>>
    <associate|auto-40|<tuple|4.3.3|15>>
    <associate|auto-41|<tuple|4.3.3|15>>
    <associate|auto-42|<tuple|4.3.3|15>>
    <associate|auto-43|<tuple|4.3.3|16>>
    <associate|auto-44|<tuple|4.3.3|17>>
    <associate|auto-45|<tuple|7.3|?>>
    <associate|auto-46|<tuple|7.4|?>>
    <associate|auto-47|<tuple|7.5|?>>
    <associate|auto-48|<tuple|8|?>>
    <associate|auto-49|<tuple|8.1|?>>
    <associate|auto-5|<tuple|1.2.2|2>>
    <associate|auto-50|<tuple|8.2|?>>
    <associate|auto-51|<tuple|8.2.1|?>>
    <associate|auto-52|<tuple|8.2.2|?>>
    <associate|auto-53|<tuple|9|?>>
    <associate|auto-54|<tuple|9.1|?>>
    <associate|auto-55|<tuple|9.1.1|?>>
    <associate|auto-56|<tuple|9.1.2|?>>
    <associate|auto-57|<tuple|10|?>>
    <associate|auto-58|<tuple|10.1|?>>
    <associate|auto-6|<tuple|1.2.3|2>>
    <associate|auto-7|<tuple|1.2.4|2>>
    <associate|auto-8|<tuple|2|2>>
    <associate|auto-9|<tuple|2.1|2>>
    <associate|backend|<tuple|1|7>>
    <associate|bib-cuckoo|<tuple|YD09|17>>
    <associate|bib-gomet|<tuple|BL10|17>>
    <associate|bib-graphite|<tuple|PCB+06|17>>
    <associate|cmdoptions|<tuple|1|3>>
    <associate|frapsched|<tuple|4.1|15>>
    <associate|frontend|<tuple|1|6>>
    <associate|kimblevisu|<tuple|1|12>>
    <associate|kroket|<tuple|4.1|15>>
    <associate|pragma|<tuple|3.3|3>>
    <associate|progcons|<tuple|3.2|14>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|table>
      <tuple|normal|Command-line options<label|cmdoptions>|<pageref|auto-12>>

      <tuple|normal|Generator Attributes|<pageref|auto-16>>

      <tuple|normal|External command hooks|<pageref|auto-24>>

      <tuple|normal|Data attributes|<pageref|auto-28>>

      <tuple|normal|Special values|<pageref|auto-29>>
    </associate>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Introduction>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>

      <with|par-left|<quote|1.5fn>|1.1<space|2spc>Motivation
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2>>

      <with|par-left|<quote|1.5fn>|1.2<space|2spc>Concepts
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-3>>

      <with|par-left|<quote|3fn>|1.2.1<space|2spc>Variant
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-4>>

      <with|par-left|<quote|3fn>|1.2.2<space|2spc>Generator
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-5>>

      <with|par-left|<quote|3fn>|1.2.3<space|2spc>Plan
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-6>>

      <with|par-left|<quote|3fn>|1.2.4<space|2spc>Loader
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-7>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|2<space|2spc>Quickstart>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-8><vspace|0.5fn>

      <with|par-left|<quote|1.5fn>|2.1<space|2spc>Installation
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-9>>

      <with|par-left|<quote|1.5fn>|2.2<space|2spc>Usage & Behavior
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-10>>

      <with|par-left|<quote|1.5fn>|2.3<space|2spc>Command-line Options
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-11>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|3<space|2spc>Mania
      Description Files> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-13><vspace|0.5fn>

      <with|par-left|<quote|1.5fn>|3.1<space|2spc>Environment Description
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-14>>

      <with|par-left|<quote|3fn>|3.1.1<space|2spc>Generator Description
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-15>>

      <with|par-left|<quote|6fn>|Cleaning
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-17><vspace|0.15fn>>

      <with|par-left|<quote|6fn>|Checking
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-18><vspace|0.15fn>>

      Builtin Generators <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-19><vspace|0.15fn>

      <with|par-left|<quote|3fn>|3.1.2<space|2spc>Variant Description
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-20>>

      <with|par-left|<quote|3fn>|3.1.3<space|2spc>Plan Description
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-21>>

      <with|par-left|<quote|6fn>|Builtin Plans
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-22><vspace|0.15fn>>

      <with|par-left|<quote|6fn>|External Commands
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-23><vspace|0.15fn>>

      <with|par-left|<quote|1.5fn>|3.2<space|2spc>Program Description
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-25>>

      <with|par-left|<quote|3fn>|3.2.1<space|2spc>Extra Source File
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-26>>

      <with|par-left|<quote|3fn>|3.2.2<space|2spc>Data List
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-27>>

      <with|par-left|<quote|6fn>|Scalar <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-30><vspace|0.15fn>>

      <with|par-left|<quote|6fn>|Array <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-31><vspace|0.15fn>>

      <with|par-left|<quote|6fn>|Structure and Union
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-32><vspace|0.15fn>>
    </associate>
  </collection>
</auxiliary>