from queue import Queue
from bears.general.CasingBear import CasingBear
from tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.bears.LocalBear import LocalBear


class CasingBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = CasingBear(self.section, Queue())

    def test_defaults(self):
        self.section.append(Setting("casing", "snake"))
        self.section.append(Setting("language", "CPP"))
        self.check_validity(self.uut, ["int abc_def;\n", "int ab_cd;\n"])
        self.check_validity(self.uut, ["int abc_def = xyz_abc;\n"])
        self.check_validity(self.uut, ["int abcEfg = 4;\n"], valid=False)
        self.check_validity(self.uut, ["int abCd = 4;\n"], valid=False)
        self.check_validity(
            self.uut,
            ["int abc_def;\n", "int abCd;\n"],
            valid=False)
        self.check_validity(
            self.uut,
            ["char wrongStr=\"test\";\n", "int correct_var = 42;\n"],
            valid=False)
        self.check_validity(
            self.uut,
            ["char correct_str=\"test\";\n", "int correct_var = 42;\n"],
            valid=True)
        self.check_validity(
            self.uut,
            ["testVar = 42;\n", "testVar = 0;\n", "testVar += 1;\n"],
            valid=False)
        self.check_validity(
            self.uut,
            ["int incorrectVar = 32, anotherInt = 22\n"],
            valid=False)
        self.check_validity(
            self.uut,
            ["int correct_var = 32, anotherInt = 22\n"],
            valid=False)
        self.check_validity(
            self.uut,
            ["int correct_var = 32, another_int = 22\n"],
            valid=True)

    def test_invalid_settings(self):
        section = Section("test_section_2")
        section.append(Setting("casing", "snake"))
        section.append(Setting("language", "InvalidLang"))
        bear = CasingBear(section, Queue())

        try:
            self.check_validity(
                bear,
                ["int testVar = 42;\n", "int correct_var = 32;\n"],
                valid=False)
        except Exception as e:
            self.assertIsInstance(e, AssertionError)

        section = Section("test_section_3")
        section.append(Setting("casing", "invalid"))
        section.append(Setting("language", "C"))
        bear = CasingBear(section, Queue())

        self.check_results(
            bear,
            ["int testVar = 42;\n"],
            results=[])

        section = Section("test_section_4")
        section.append(Setting("casing", "snake"))
        section.append(Setting("language", "python3"))
        bear = CasingBear(section, Queue())

        self.check_results(
            bear,
            ["testVar = 42\n"],
            results=[])
