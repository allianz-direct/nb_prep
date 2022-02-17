import subprocess

# mkdocs-macros-plugin
# add a {{ last_git_ tag }} to markdown pages
def define_env(env):
  "Hook function"

  @env.macro
  def last_git_tag():
      result = subprocess.run(['git', 'describe','--tags','--abbrev=0'], stdout=subprocess.PIPE)
      return result.stdout.decode('utf-8').strip()