import ant

from twisted.trial import unittest
from buildbot.status.results import SKIPPED, SUCCESS, WARNINGS, FAILURE
from buildbot.test.util import steps, compat

class FakeLogFile:
    def __init__(self, text):
        self.text = text

    def getText(self):
        return self.text

class FakeCmd:
    def __init__(self, stdout, stderr, rc=0):
        self.logs = {'stdout': FakeLogFile(stdout),
                     'stderr': FakeLogFile(stderr)}
        self.rc = rc

class TestAnt(steps.BuildStepMixin, unittest.TestCase):

    def setUp(self):
        return self.setUpBuildStep()

    def tearDown(self):
        return self.tearDownBuildStep()
        
    def test_dzilPass(self):
        step = self.setupStep(ant.AntTest())
        
        log = """junit:
    [mkdir] Created dir: /Users/buildbot/oss-slave/ant-task-sitemap/build/report/junit/xml
    [junit] Running uk.co.arjones.ant.task.SitemapTest
    [junit] Tests run: 1, Failures: 0, Errors: 0, Time elapsed: 0.539 sec

junitreport:
    [mkdir] Created dir: /Users/buildbot/oss-slave/ant-task-sitemap/build/report/junit/html
[junitreport] Processing /Users/buildbot/oss-slave/ant-task-sitemap/build/report/junit/html/TESTS-TestSuites.xml to /var/folders/bv/4c_z4wmd7h92bc6llrm6fcgm0000gp/T/null1009356432
[junitreport] Loading stylesheet jar:file:/usr/share/ant/lib/ant-junit.jar!/org/apache/tools/ant/taskdefs/optional/junit/xsl/junit-frames.xsl
[junitreport] Transform time: 552ms
[junitreport] Deleting: /var/folders/bv/4c_z4wmd7h92bc6llrm6fcgm0000gp/T/null1009356432

test:

BUILD SUCCESSFUL
Total time: 3 seconds"""
        step.addCompleteLog('stdio', log)

        rc = step.evaluateCommand(FakeCmd("", ""))
        
        self.assertEqual(rc, SUCCESS)
        self.assertEqual(self.step_statistics, {
            'tests-total' : 1,
            'tests-failed' : 0,
            'tests-passed' : 1,
            'tests-warnings' : 0,
        })
        
    def test_dzilFailure(self):
        step = self.setupStep(ant.AntTest())
        
        log = """junit:
    [mkdir] Created dir: /Users/buildbot/oss-slave/ant-task-sitemap/build/report/junit/xml
    [junit] Running uk.co.arjones.ant.task.SitemapTest
    [junit] Tests run: 1, Failures: 1, Errors: 0, Time elapsed: 0.539 sec

junitreport:
    [mkdir] Created dir: /Users/buildbot/oss-slave/ant-task-sitemap/build/report/junit/html
[junitreport] Processing /Users/buildbot/oss-slave/ant-task-sitemap/build/report/junit/html/TESTS-TestSuites.xml to /var/folders/bv/4c_z4wmd7h92bc6llrm6fcgm0000gp/T/null1009356432
[junitreport] Loading stylesheet jar:file:/usr/share/ant/lib/ant-junit.jar!/org/apache/tools/ant/taskdefs/optional/junit/xsl/junit-frames.xsl
[junitreport] Transform time: 552ms
[junitreport] Deleting: /var/folders/bv/4c_z4wmd7h92bc6llrm6fcgm0000gp/T/null1009356432

test:

BUILD SUCCESSFUL
Total time: 3 seconds"""
        step.addCompleteLog('stdio', log)
        
        rc = step.evaluateCommand(FakeCmd("", ""))
        
        self.assertEqual(rc, FAILURE)
        self.assertEqual(self.step_statistics, {
            'tests-total' : 1,
            'tests-failed' : 1,
            'tests-passed' : 0,
            'tests-warnings' : 0,
        })
