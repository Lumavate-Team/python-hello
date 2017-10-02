import os
import re

class PwaBehavior:
  def load_precache_files(self, filters=None):
    filters = filters or []
    root_dir = '/app/dist/'

    def is_valid(f):
      if not filters:
        return True

      return bool(next(filter(lambda exp: re.search(exp, f), filters), None))

    return [f for f in os.listdir(root_dir)
      if os.path.isfile(os.path.join(root_dir, f)) and is_valid(f)]

  def is_versioned(self, filename, filters=None):
    filters = filters or ['bundle']

    return bool(next(filter(lambda exp: re.search(exp, filename), filters), None))

  def get_revision(self):
    git_revision = open('/revision', 'r')
    commit_hash = git_revision.readline().strip('\n')
    git_revision.close()

    return commit_hash
