from handyscikit import cprint, suppress_stdout


class PrintRelatedTest:
    @staticmethod
    def cprint():
        cprint("[Cprint Test] Test passed", color="green")

    @staticmethod
    def suppress_stdout():
        with suppress_stdout():
            cprint("If you see this, means test failed.")

        cprint("[SuppressStdout Test] Test passed", color="green")


if __name__ == "__main__":
    PrintRelatedTest.cprint()
    PrintRelatedTest.suppress_stdout()
