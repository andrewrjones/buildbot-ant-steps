buildbot-dzil-steps
===================

Buildbot build steps optimised for ant, the Java build tool.

Currently only 'test' is implemented.

Usage
-----

Firstly, download or clone the code and put it somewhere near your buildmaster.

Then add the following (or similar):

    from ant import AntTest

### AntTest()

You can use this as follows:

    factory.addStep(AntTest())

It will run the `ant test` command in the build directory. The output is then parsed to get the test results, which are then displayed in your waterfall.

It is a subclass of `Test`, and takes the same arguments.

TODO
----
- Upload JUnit HTML output
