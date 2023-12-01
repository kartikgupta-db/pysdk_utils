import subprocess
import sys
import platform
import re

class DIPConnect:
    def __init__(self, workspace_url, setup_fl = False, profile : str = ""):
        # Initialize any required variables
        self.workspace_url = workspace_url
        self.setup_fl = setup_fl
        self.profile = profile

    def setup_environment(self):
        # Shell command for Databricks authentication
        cli_command = "databricks configure {}".format(self.workspace_url)

        try:
            # Run the shell command
            subprocess.run(cli_command, shell=True, check=True)
            print("Authentication successful.")
        except subprocess.CalledProcessError as e:
            # Handle errors in the authentication process
            print(f"An error occurred during authentication: {e}")

    def __get_prefix(self):

        # Regex pattern
        pattern = r'https://([^\.]+)'

        # Search for the pattern
        match = re.search(pattern, self.workspace_url)

        # Extract the matched part
        if match:
            result = match.group(1)
            return(result)
        else:
            print("Workspace URL pattern not found")

    def authenticate(self):
        # Shell command for Databricks authentication
        auth_command = "/usr/local/bin/databricks auth login --host {}".format(self.workspace_url)

        try:
            # Choose the right module based on the OS
            if platform.system() == 'Windows':
                import wexpect as expect
            else:
                import pexpect as expect

            # Start the command with pexpect
            child = expect.spawn(auth_command)

            # Wait for the prompt where the profile needs to be entered
            # Note: Replace 'Prompt text' with the actual text that the command
            # prompts you with before you need to enter the profile name
            # Send the profile name
            if len(self.profile) > 0:
                prefix = self.__get_prefix()
                for l in prefix:
                    child.send('\b')
                child.sendline(self.profile)

            else:
                child.sendline('\n')

            # Optional: Wait for any follow-up prompts and send responses in a similar way
            # child.expect('Next prompt text')
            # child.sendline('response to next prompt')

            # Wait for the command to complete
            child.expect(expect.EOF)

            # Get the output
            stdout = child.before.decode()

            if stdout:
                print("Authentication successful. Output:", stdout)
            else:
                print("Authentication unsuccessful or no output.")

        except expect.ExceptionPexpect as e:
            # Handle errors in the authentication process
            print(f"An error occurred during authentication: {e}")

    def setup_profile(self):
        import os
        os.environ['DATABRICKS_CONFIG_PROFILE'] = self.profile

    def connect(self):
        if self.setup_fl:
           self.setup_environment()
        self.authenticate()
        self.setup_profile()